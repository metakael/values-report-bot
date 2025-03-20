#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database module for Firebase integration
"""

import logging
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from config import Config

logger = logging.getLogger(__name__)

# In-memory storage as fallback
_memory_access_codes = {
    "TEST123": 10,
    "DEMO456": 5,
    "TESTALT": 15
}

_memory_users = {}
_memory_reports = {}

# Initialize Firebase (if credentials exist)
try:
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if cred_path and os.path.exists(cred_path):
        # Use credential file path
        cred = credentials.Certificate(cred_path)
    elif hasattr(Config, 'FIREBASE_CREDENTIALS_JSON') and Config.FIREBASE_CREDENTIALS_JSON:
        # Use JSON string from environment variable
        cred_dict = json.loads(Config.FIREBASE_CREDENTIALS_JSON)
        cred = credentials.Certificate(cred_dict)
    else:
        # No credentials available
        logger.warning("Firebase credentials not found - using memory storage only")
        cred = None
        db = None
    
    if cred:
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info("Firebase connection established successfully")
except Exception as e:
    logger.error(f"Firebase initialization error: {e}")
    db = None

def init_db():
    """Initialize database connection and verify collections"""
    try:
        if db:
            # Try to access a collection to verify connection
            access_codes_ref = db.collection('access_codes')
            access_codes_ref.limit(1).get()
            logger.info("Database connection established successfully")
            return True
        else:
            logger.warning("Using memory-based storage due to Firebase connection issues")
            return False
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        logger.warning("Falling back to memory-based storage")
        return False

def verify_access_code(code):
    """
    Verify if an access code is valid and has remaining uses
    
    Args:
        code (str): Access code provided by the user
        
    Returns:
        bool: True if valid code with remaining uses, False otherwise
        int: Remaining uses after this use (None if invalid)
    """
    try:
        logger.info(f"Attempting to verify access code: {code}")
        
        # Check memory-based access codes first
        if code in _memory_access_codes and _memory_access_codes[code] > 0:
            remaining = _memory_access_codes[code]
            _memory_access_codes[code] -= 1
            logger.info(f"Valid code found in memory: {code} (remaining: {remaining-1})")
            return True, remaining - 1
        
        # Try Firebase verification as backup
        if db:
            try:
                # Query for the access code
                access_codes_ref = db.collection('access_codes')
                query = access_codes_ref.where('code', '==', code).limit(1)
                results = query.get()
                
                for doc in results:
                    code_data = doc.to_dict()
                    remaining_uses = code_data.get('remaining_uses', 0)
                    logger.info(f"Found code in Firebase with remaining uses: {remaining_uses}")
                    
                    if remaining_uses > 0:
                        # Update remaining uses
                        doc_ref = access_codes_ref.document(doc.id)
                        doc_ref.update({'remaining_uses': remaining_uses - 1})
                        logger.info(f"Updated remaining uses for code: {code}")
                        return True, remaining_uses - 1
                    else:
                        logger.info(f"Code found but has no remaining uses: {code}")
                        return False, None
                
                logger.info(f"Code not found in Firebase: {code}")
            except Exception as db_err:
                logger.error(f"Firebase verification failed: {db_err}")
        
        return False, None
    
    except Exception as e:
        logger.error(f"Error verifying access code: {e}")
        return False, None

def store_user_data(user_id, user_data):
    """
    Store user data in memory with Firebase fallback
    
    Args:
        user_id (int): Telegram user ID
        user_data (dict): User data containing values and personal information
        
    Returns:
        bool: True if successful, False otherwise
        str: Record ID if successful, None otherwise
    """
    try:
        # Store in memory
        _memory_users[user_id] = user_data.copy()
        logger.info(f"User data stored in memory for user {user_id}")
        
        # Try Firebase storage as backup
        if db:
            try:
                # Prepare data for Firebase
                storage_data = {
                    'telegram_id': user_id,
                    'telegram_username': user_data.get('telegram_username'),
                    'top_values': user_data.get('top_values', []),
                    'next_values': user_data.get('next_values', []),
                    'age': user_data.get('age'),
                    'country': user_data.get('country'),
                    'occupation': user_data.get('occupation'),
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'updated_at': firestore.SERVER_TIMESTAMP
                }
                
                # Check if user already exists
                users_ref = db.collection('users')
                query = users_ref.where('telegram_id', '==', user_id).limit(1)
                results = query.get()
                
                if len(results) > 0:
                    # User exists, update
                    doc_ref = users_ref.document(results[0].id)
                    storage_data['updated_at'] = firestore.SERVER_TIMESTAMP  # Update timestamp
                    doc_ref.update(storage_data)
                    logger.info(f"User data updated in Firebase for user {user_id}")
                    return True, results[0].id
                else:
                    # Create new user
                    doc_ref = users_ref.add(storage_data)
                    logger.info(f"User data added to Firebase for user {user_id}")
                    return True, doc_ref[1].id
            except Exception as db_err:
                logger.error(f"Firebase storage failed: {db_err}")
        
        return True, str(user_id)
    
    except Exception as e:
        logger.error(f"Error storing user data: {e}")
        return False, None

def store_report(user_id, report_data):
    """
    Store generated report data
    
    Args:
        user_id (int): Telegram user ID
        report_data (dict): Report data including prompts and responses
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Store in memory
        if user_id not in _memory_reports:
            _memory_reports[user_id] = []
        
        _memory_reports[user_id].append(report_data.copy())
        logger.info(f"Report data stored in memory for user {user_id}")
        
        # Try Firebase storage as backup
        if db:
            try:
                reports_ref = db.collection('reports')
                
                # Prepare data for Firebase
                fb_report_data = {
                    'telegram_id': user_id,
                    'sections_content': report_data.get('sections_content', {}),
                    'prompts_used': report_data.get('prompts_used', {}),
                    'generation_date': firestore.SERVER_TIMESTAMP
                }
                
                # Add to Firestore
                doc_ref = reports_ref.add(fb_report_data)
                logger.info(f"Report data stored in Firebase for user {user_id}")
                
                # Also store in user_sessions collection
                users_ref = db.collection('users')
                query = users_ref.where('telegram_id', '==', user_id).limit(1)
                results = query.get()
                
                if len(results) > 0:
                    user_doc_id = results[0].id
                    user_data = results[0].to_dict()
                    
                    sessions_ref = db.collection('user_sessions')
                    session_data = {
                        'user_id': user_doc_id,
                        'telegram_id': user_id,
                        'access_code': user_data.get('access_code', 'unknown'),
                        'top_values': user_data.get('top_values', []),
                        'next_values': user_data.get('next_values', []),
                        'age': user_data.get('age'),
                        'country': user_data.get('country'),
                        'occupation': user_data.get('occupation'),
                        'session_start': firestore.SERVER_TIMESTAMP,
                        'session_end': firestore.SERVER_TIMESTAMP,
                        'report_ref': doc_ref[1]
                    }
                    
                    sessions_ref.add(session_data)
                    logger.info(f"Session data stored in Firebase for user {user_id}")
            except Exception as db_err:
                logger.error(f"Firebase report storage failed: {db_err}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error storing report data: {e}")
        return False

def add_access_code(code, remaining_uses=5):
    """
    Add a new access code to the database
    
    Args:
        code (str): Access code to add
        remaining_uses (int): Number of times the code can be used
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Add to memory storage
        _memory_access_codes[code] = remaining_uses
        logger.info(f"Access code added to memory: {code} (uses: {remaining_uses})")
        
        # Add to Firebase
        if db:
            try:
                access_codes_ref = db.collection('access_codes')
                
                # Check if code already exists
                query = access_codes_ref.where('code', '==', code).limit(1)
                results = query.get()
                
                if len(results) > 0:
                    # Update existing code
                    doc_ref = access_codes_ref.document(results[0].id)
                    doc_ref.update({'remaining_uses': remaining_uses})
                    logger.info(f"Access code updated in Firebase: {code}")
                else:
                    # Add new code
                    access_codes_ref.add({
                        'code': code,
                        'remaining_uses': remaining_uses,
                        'created_at': firestore.SERVER_TIMESTAMP
                    })
                    logger.info(f"Access code added to Firebase: {code}")
                
                return True
            except Exception as db_err:
                logger.error(f"Firebase access code storage failed: {db_err}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error adding access code: {e}")
        return False