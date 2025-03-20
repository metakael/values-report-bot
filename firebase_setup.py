#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Firebase Setup Script for Values Report Bot
This script initializes the Firebase database with necessary collections and test data.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_firebase():
    """Setup Firebase database with initial collections and test data"""
    
    print("Initializing Firebase setup...")
    
    # Initialize Firebase
    try:
        cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if cred_path and os.path.exists(cred_path):
            # Use credential file path
            cred = credentials.Certificate(cred_path)
            print(f"Using credentials from file: {cred_path}")
        elif os.environ.get('FIREBASE_CREDENTIALS_JSON'):
            # Use JSON string from environment variable
            cred_dict = json.loads(os.environ.get('FIREBASE_CREDENTIALS_JSON'))
            cred = credentials.Certificate(cred_dict)
            print("Using credentials from environment variable")
        else:
            print("Error: No Firebase credentials found")
            print("Please set either GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_CREDENTIALS_JSON")
            return False
        
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase connection established successfully")
        
        # Create collections and initial data
        setup_collections(db)
        return True
    
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        return False

def setup_collections(db):
    """Create necessary collections and add test data"""
    
    # Create access_codes collection with test codes
    print("Setting up access_codes collection...")
    access_codes_ref = db.collection('access_codes')
    
    test_codes = [
        {"code": "TEST123", "remaining_uses": 10, "created_at": firestore.SERVER_TIMESTAMP},
        {"code": "DEMO456", "remaining_uses": 5, "created_at": firestore.SERVER_TIMESTAMP},
        {"code": "TESTALT", "remaining_uses": 15, "created_at": firestore.SERVER_TIMESTAMP}
    ]
    
    for code_data in test_codes:
        # Check if code already exists
        query = access_codes_ref.where('code', '==', code_data["code"]).limit(1)
        results = query.get()
        
        if len(results) == 0:
            # Add new code
            access_codes_ref.add(code_data)
            print(f"Added access code: {code_data['code']}")
        else:
            # Update existing code
            doc_ref = access_codes_ref.document(results[0].id)
            doc_ref.update({"remaining_uses": code_data["remaining_uses"]})
            print(f"Updated access code: {code_data['code']}")
    
    # Create empty users collection if it doesn't exist
    print("Setting up users collection...")
    users_ref = db.collection('users')
    query = users_ref.limit(1).get()
    if len(query) == 0:
        print("Users collection is empty and ready for use")
    else:
        print(f"Users collection exists with data ({len(query)} samples)")
    
    # Create empty reports collection if it doesn't exist
    print("Setting up reports collection...")
    reports_ref = db.collection('reports')
    query = reports_ref.limit(1).get()
    if len(query) == 0:
        print("Reports collection is empty and ready for use")
    else:
        print(f"Reports collection exists with data ({len(query)} samples)")
    
    # Create empty user_sessions collection if it doesn't exist
    print("Setting up user_sessions collection...")
    sessions_ref = db.collection('user_sessions')
    query = sessions_ref.limit(1).get()
    if len(query) == 0:
        print("User_sessions collection is empty and ready for use")
    else:
        print(f"User_sessions collection exists with data ({len(query)} samples)")
    
    print("Firebase setup completed successfully!")

if __name__ == "__main__":
    setup_firebase()