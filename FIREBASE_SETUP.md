# Firebase Setup Guide for Values Report Bot

This guide provides detailed instructions for setting up Firebase for your Values Report Telegram Bot.

## Creating a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click "Add project" to create a new project.
3. Enter a project name (e.g., "values-report-bot").
4. Choose whether to enable Google Analytics (optional).
5. Click "Create project" and wait for the setup to complete.

## Enabling Firestore Database

1. In the Firebase Console, select your project.
2. In the left sidebar, click "Firestore Database".
3. Click "Create database".
4. Choose "Start in production mode" and select a database location close to your users.
5. Click "Enable".

## Generating Service Account Credentials

1. In the Firebase Console, go to "Project settings" (gear icon in the top left).
2. Select the "Service accounts" tab.
3. Under "Firebase Admin SDK", click "Generate new private key".
4. Save the JSON file securely - this contains sensitive information.

## Setting Up Environment Variables

### For Local Development

1. Set the path to your service account JSON file as an environment variable:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account-file.json
   ```

### For Render Deployment

1. Convert your service account JSON file to a single-line string:
   - Open the JSON file
   - Remove all line breaks and extra spaces to make it a single line
   - Properly escape quotes and special characters

2. Add this string as the `FIREBASE_CREDENTIALS_JSON` environment variable in Render.

## Running the Firebase Setup Script

The `firebase_setup.py` script initializes your Firebase database with the necessary collections and test data:

1. Ensure your environment variables are properly set.
2. Run the script:
   ```bash
   python firebase_setup.py
   ```

3. The script will create:
   - `access_codes` collection with test codes
   - Empty `users` collection
   - Empty `reports` collection
   - Empty `user_sessions` collection

## Firebase Database Structure

Your Firebase database will have the following collections:

### access_codes
- Documents containing:
  - `code`: String - the access code
  - `remaining_uses`: Number - how many times it can be used
  - `created_at`: Timestamp - when it was created

### users
- Documents containing:
  - `telegram_id`: Number - user's Telegram ID
  - `telegram_username`: String - user's Telegram username
  - `top_values`: Array - ranked values (positions 1-5)
  - `next_values`: Array - unranked values (positions 6-10)
  - `age`: Number - user's age
  - `country`: String - user's country
  - `occupation`: String - user's occupation
  - `created_at`: Timestamp - when user was first added
  - `updated_at`: Timestamp - when user was last updated

### reports
- Documents containing:
  - `telegram_id`: Number - user's Telegram ID
  - `sections_content`: Map - content for each report section
  - `prompts_used`: Map - prompts used for each section
  - `generation_date`: Timestamp - when report was generated

### user_sessions
- Documents containing:
  - `user_id`: String - reference to user document ID
  - `telegram_id`: Number - user's Telegram ID
  - `access_code`: String - access code used
  - `top_values`: Array - ranked values (positions 1-5)
  - `next_values`: Array - unranked values (positions 6-10)
  - `age`: Number - user's age
  - `country`: String - user's country
  - `occupation`: String - user's occupation
  - `session_start`: Timestamp - when session started
  - `session_end`: Timestamp - when report was generated
  - `report_ref`: Reference - reference to the report document

## Security Rules

By default, Firebase Firestore uses secure rules that only allow authenticated access. For a Telegram bot backend, you'll be using service account authentication which bypasses these rules.

For additional security, you may want to set up custom security rules:

1. In the Firebase Console, go to "Firestore Database".
2. Click on the "Rules" tab.
3. Use the following rules as a starting point:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Lock down all access except through authenticated service account
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

## Troubleshooting

### Invalid Service Account Credentials
- Ensure the JSON file is complete and valid
- Check that the environment variable points to the correct file
- For Render, make sure the JSON string is properly escaped

### Missing Collections
- Run the `firebase_setup.py` script to initialize collections
- Check console output for any errors

### Permission Denied Errors
- Verify that your service account has the necessary permissions
- Check if Firestore is enabled in your Firebase project
- Ensure your project ID in credentials matches your actual project