#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database module for Supabase integration
"""

import logging
from supabase import create_client
from config import Config

logger = logging.getLogger(__name__)

# Initialize Supabase client
import os
os.environ["SUPABASE_URL"] = Config.SUPABASE_URL
os.environ["SUPABASE_KEY"] = Config.SUPABASE_KEY
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def init_db():
    """Initialize database connection and verify tables"""
    try:
        # Test the connection
        response = supabase.table('access_codes').select('*').limit(1).execute()
        logger.info("Database connection established successfully")
        return True
    except Exception as e:
        logger.error(f"Database connection error: {e}")
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
        response = supabase.table('access_codes').select('*').eq('code', code).execute()
        
        logger.info(f"Database response: {response}")
        
        # Check if code exists and has remaining uses
        if response.data and len(response.data) > 0:
            code_data = response.data[0]
            remaining_uses = code_data.get('remaining_uses', 0)
            logger.info(f"Found code with remaining uses: {remaining_uses}")
            
            if remaining_uses > 0:
                # Decrement remaining uses
                logger.info(f"Decrementing remaining uses for code: {code}")
                update_response = supabase.table('access_codes').update(
                    {'remaining_uses': remaining_uses - 1}
                ).eq('code', code).execute()
                
                logger.info(f"Update response: {update_response}")
                return True, remaining_uses - 1
            else:
                logger.info(f"Code found but has no remaining uses: {code}")
        else:
            logger.info(f"Code not found: {code}")
        
        return False, None
    
    except Exception as e:
        logger.error(f"Error verifying access code: {e}")
        return False, None

def store_user_data(user_id, user_data):
    """
    Store user data in the database
    
    Args:
        user_id (int): Telegram user ID
        user_data (dict): User data containing values and personal information
        
    Returns:
        bool: True if successful, False otherwise
        str: Record ID if successful, None otherwise
    """
    try:
        # Check if user already exists
        existing = supabase.table('users').select('*').eq('telegram_id', user_id).execute()
        
        if existing.data and len(existing.data) > 0:
            # Update existing user
            response = supabase.table('users').update(user_data).eq('telegram_id', user_id).execute()
            return True, response.data[0]['id'] if response.data else None
        else:
            # Insert new user
            user_data['telegram_id'] = user_id
            response = supabase.table('users').insert(user_data).execute()
            return True, response.data[0]['id'] if response.data else None
    
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
        report_data['telegram_id'] = user_id
        response = supabase.table('reports').insert(report_data).execute()
        return True
    
    except Exception as e:
        logger.error(f"Error storing report data: {e}")
        return False