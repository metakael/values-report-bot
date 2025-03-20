# Personal Values Report Telegram Bot

A Telegram bot that creates personalized values reports based on user inputs. The bot collects users' top 10 values (with the top 5 ranked), along with age, country, and occupation information. It then uses Google Gemini's LLM to generate a comprehensive values analysis report delivered as a professionally formatted PDF.

## Features

- **User Verification**: Access code validation for authorized users
- **Data Collection**: Collects values (top 5 ranked, next 5 unranked) and personal information
- **Content Generation**: Generates personalized content using Google Gemini API
- **PDF Generation**: Creates professional PDF reports with consistent formatting
- **Secure Storage**: Stores user data in Firebase for future reference and analysis

## Technology Stack

- **Language**: Python
- **Bot Framework**: python-telegram-bot
- **Database**: Firebase Firestore
- **LLM API**: Google Gemini
- **PDF Generation**: WeasyPrint with Jinja2 templates
- **Deployment**: Render

## Project Structure

```
values_report_bot/
├── app.py                 # Main application entry point
├── config.py              # Configuration and environment variables
├── firebase_setup.py      # Firebase initialization script
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not tracked in git)
├── .env.template          # Template for environment variables
├── modules/
│   ├── bot_handler.py     # Telegram bot conversation handlers
│   ├── database.py        # Firebase integration and database operations
│   ├── llm_integration.py # Google Gemini API integration
│   ├── pdf_generator.py   # WeasyPrint PDF generation
│   └── utils.py           # Utility functions
├── static/
│   ├── css/               # CSS for PDF styling
│   ├── images/            # Logo and other assets
│   └── fonts/             # Poppins font files
└── templates/
    └── report_template.html  # Jinja2 template for PDF
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Telegram Bot token (from BotFather)
- Firebase project with Firestore database
- Google Gemini API key
- Render account (for deployment)

### Firebase Setup

1. Create a Firebase project:
   - Go to the [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" and follow the setup wizard
   - Enable Firestore Database from the left sidebar

2. Generate service account credentials:
   - In your Firebase project, go to Project Settings > Service accounts
   - Click "Generate new private key"
   - Save the JSON file securely

3. Initialize Firebase collections:
   - Place your service account JSON file in a secure location
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of this file
   - Run the setup script: `python firebase_setup.py`

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd values_report_bot
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.template .env
   ```
   Edit the `.env` file and add your API keys and configuration.

5. Create the static directory and add necessary assets:
   ```bash
   mkdir -p static/images static/fonts
   ```
   
   - Add your logo to `static/images/logo.png`
   - Add Poppins font files to `static/fonts/`

6. Run the bot locally:
   ```bash
   python app.py
   ```

### Deployment to Render

1. Create a new Web Service on Render linked to your GitHub repository.

2. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment Variables**: Add all variables from your `.env` file, including:
     - `TELEGRAM_TOKEN`
     - `FIREBASE_CREDENTIALS_JSON` (copy the entire content of your service account JSON file)
     - `GEMINI_API_KEY`
     - `WEBHOOK_URL` (set to your Render deployment URL)

3. Deploy the service.

## Bot Usage Flow

1. User starts the bot with `/start` command
2. Bot requests an access code for verification
3. Once verified, bot collects top 5 ranked values
4. Bot collects next 5 values (unranked)
5. Bot collects personal information (age, country, occupation)
6. User reviews and confirms the collected information
7. Bot generates the personalized values report PDF
8. PDF is delivered to the user via Telegram

## Maintenance and Support

To add or update access codes, you can either:

1. Use the Firebase Console to directly add documents to the `access_codes` collection
2. Run the `firebase_setup.py` script with updated code information
3. Use the `add_access_code()` function from the database module

## License

[Specify your license here]

## Contributors

[Your name/organization]