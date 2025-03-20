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
    """
    try:
        logger.info(f"Attempting to verify access code: {code}")
        
        # Development override for testing
        if code in ["TEST123", "DEMO456"]:
            logger.info(f"Using development override for {code}")
            return True, 10
        
        # Test connection and permissions with a basic query
        try:
            logger.info("Testing basic database access...")
            test_response = supabase.from_('access_codes').select('*').limit(5).execute()
            logger.info(f"Basic access test response: {test_response}")
        except Exception as conn_err:
            logger.error(f"Basic database access failed: {conn_err}")
        
        # Try alternative query format
        try:
            logger.info(f"Trying alternative query format for code: {code}")
            alt_response = supabase.from_('access_codes').select('*').filter('code', 'eq', code).execute()
            logger.info(f"Alternative query response: {alt_response}")
            
            if alt_response.data and len(alt_response.data) > 0:
                code_data = alt_response.data[0]
                remaining_uses = code_data.get('remaining_uses', 0)
                
                if remaining_uses > 0:
                    update_response = supabase.from_('access_codes').update({
                        'remaining_uses': remaining_uses - 1
                    }).eq('id', code_data.get('id')).execute()
                    
                    return True, remaining_uses - 1
        except Exception as alt_err:
            logger.error(f"Alternative query failed: {alt_err}")
        
        # Original query as fallback
        response = supabase.table('access_codes').select('*').eq('code', code).execute()
        logger.info(f"Original query response: {response}")
        
        if response.data and len(response.data) > 0:
            code_data = response.data[0]
            remaining_uses = code_data.get('remaining_uses', 0)
            
            if remaining_uses > 0:
                update_response = supabase.table('access_codes').update({
                    'remaining_uses': remaining_uses - 1
                }).eq('code', code).execute()
                
                return True, remaining_uses - 1
        
        return False, None
    
    except Exception as e:
        logger.error(f"Error verifying access code: {e}")
        # Fallback for testing
        if code in ["TEST123", "DEMO456"]:
            return True, 10
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