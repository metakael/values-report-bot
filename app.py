#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram Bot for Personal Values Report
Main application entry point
"""

import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from modules.bot_handler import (
    start, handle_access_code, 
    collect_top_five_values, collect_next_five_values, 
    collect_age, collect_country, collect_occupation,
    review_inputs, confirm_inputs, generate_report, cancel
)
from modules.database import init_db
from config import Config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
(
    ACCESS_CODE, 
    TOP_FIVE_VALUES, NEXT_FIVE_VALUES, 
    AGE, COUNTRY, OCCUPATION, 
    REVIEW, GENERATING_REPORT
) = range(8)

def main():
    """Start the bot."""
    # Create the Application
    updater = Updater(Config.TELEGRAM_TOKEN)
    application = updater.dispatcher

    # Initialize database
    init_db()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACCESS_CODE: [MessageHandler(Filters.text & ~Filters.command, handle_access_code)],
            TOP_FIVE_VALUES: [MessageHandler(Filters.text & ~Filters.command, collect_top_five_values)],
            NEXT_FIVE_VALUES: [MessageHandler(Filters.text & ~Filters.command, collect_next_five_values)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, collect_age)],
            COUNTRY: [MessageHandler(Filters.text & ~Filters.command, collect_country)],
            OCCUPATION: [MessageHandler(Filters.text & ~Filters.command, collect_occupation)],
            REVIEW: [
                CallbackQueryHandler(collect_top_five_values, pattern='^edit_top_five$'),
                CallbackQueryHandler(collect_next_five_values, pattern='^edit_next_five$'),
                CallbackQueryHandler(collect_age, pattern='^edit_age$'),
                CallbackQueryHandler(collect_country, pattern='^edit_country$'),
                CallbackQueryHandler(collect_occupation, pattern='^edit_occupation$'),
                CallbackQueryHandler(confirm_inputs, pattern='^confirm$')
            ],
            GENERATING_REPORT: [MessageHandler(Filters.text & ~Filters.command, generate_report)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="values_report_conversation",
        persistent=False,
    )

    # Add the conversation handler to the application
    application.add_handler(conv_handler)

    # Start the Bot
    if Config.WEBHOOK_URL:
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)),
            url_path=Config.TELEGRAM_TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.TELEGRAM_TOKEN}"
        )
        updater.idle()
    else:
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()