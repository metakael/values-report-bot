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
    try:
        logger.info(f"Attempting to verify access code: {code}")
        
        # Try with explicit query to troubleshoot
        query = f"select * from access_codes where code = '{code}'"
        response = supabase.rpc('select_access_code', {'query_text': query}).execute()
        
        logger.info(f"Explicit query response: {response}")
        
        # Fall back to simpler query if needed
        if not response.data or len(response.data) == 0:
            logger.info("RPC failed, trying direct table query")
            response = supabase.table('access_codes').select('*').execute()
            logger.info(f"All access codes response: {response}")
            
            # Manually filter for the code
            matching_codes = [item for item in response.data if item.get('code') == code]
            if matching_codes:
                code_data = matching_codes[0]
                remaining_uses = code_data.get('remaining_uses', 0)
                logger.info(f"Found code with remaining uses: {remaining_uses}")
                
                if remaining_uses > 0:
                    update_response = supabase.table('access_codes').update(
                        {'remaining_uses': remaining_uses - 1}
                    ).eq('id', code_data.get('id')).execute()
                    
                    logger.info(f"Update response: {update_response}")
                    return True, remaining_uses - 1
        
        return False, None
    
    except Exception as e:
        logger.error(f"Error verifying access code: {e}", exc_info=True)
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