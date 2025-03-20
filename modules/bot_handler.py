#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram Bot Handler for Values Report Bot
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from modules.database import verify_access_code, store_user_data, store_report
from modules.llm_integration import generate_all_sections, get_value_info
from modules.pdf_generator import generate_pdf, cleanup_pdf
from modules.utils import (
    parse_values, validate_age, validate_country, 
    validate_occupation, format_values_for_display
)

logger = logging.getLogger(__name__)

# Define conversation states
(
    ACCESS_CODE, 
    TOP_FIVE_VALUES, NEXT_FIVE_VALUES, 
    AGE, COUNTRY, OCCUPATION, 
    REVIEW, GENERATING_REPORT
) = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask for access code"""
    # Initialize user data storage in context
    context.user_data.clear()
    context.user_data['telegram_id'] = update.effective_user.id
    context.user_data['telegram_username'] = update.effective_user.username
    
    await update.message.reply_text(
        "Welcome to your Personal Values Report Generator! 🌟\n\n"
        "Thanks for taking part in the Knowing My Values exercise. We've set up a bot to help you generate a personalised report based on your top 10 values.\n\n"
        "Please enter your access code to begin. If you don't have one, please contact the administrator."
    )
    
    return ACCESS_CODE

async def handle_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Verify the access code provided by the user"""
    access_code = update.message.text.strip()
    
    # Verify the access code
    is_valid, remaining_uses = verify_access_code(access_code)
    
    if not is_valid:
        await update.message.reply_text(
            "⚠️ Invalid access code. Please check your code and try again, or contact the administrator."
        )
        return ACCESS_CODE
    
    # Store the access code
    context.user_data['access_code'] = access_code
    
    # Proceed to collect values
    await update.message.reply_text(
        f"✅ Access code verified! You can now proceed with creating your values report.\n\n"
        f"Let's start with your top 5 values in ranked order (1st to 5th).\n\n"
        f"Please enter your top 5 values, separated by commas, in order of importance:"
    )
    
    return TOP_FIVE_VALUES

async def collect_top_five_values(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collect the top 5 ranked values from the user"""
    # Check if this is a callback query (edit request)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Let's update your top 5 values in ranked order (1st to 5th).\n\n"
            "Please enter your top 5 values, separated by commas, in order of importance:"
        )
        return TOP_FIVE_VALUES
    
    # Parse values from text input
    values = parse_values(update.message.text)
    
    # Validate we have at least 5 values
    if len(values) < 5:
        await update.message.reply_text(
            "⚠️ Please provide at least 5 values, separated by commas, in order of importance (1st to 5th)."
        )
        return TOP_FIVE_VALUES
    
    # Store only the first 5 values
    top_values = values[:5]
    context.user_data['top_values'] = top_values
    
    # Get Schwartz categories for each value
    schwartz_categories = []
    for value in top_values:
        _, schwartz_cat, _ = get_value_info(value)
        schwartz_categories.append(schwartz_cat if schwartz_cat else "Unknown")
    
    context.user_data['schwartz_categories'] = schwartz_categories
    
    # Continue to next five values
    await update.message.reply_text(
        f"Great! Your top 5 values in order are:\n"
        f"1. {top_values[0]}\n"
        f"2. {top_values[1]}\n"
        f"3. {top_values[2]}\n"
        f"4. {top_values[3]}\n"
        f"5. {top_values[4]}\n\n"
        f"Now, please enter your next 5 values (positions 6-10) in no particular order:"
    )
    
    return NEXT_FIVE_VALUES

async def collect_next_five_values(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collect the next 5 values (not ranked) from the user"""
    # Check if this is a callback query (edit request)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Let's update your next 5 values (positions 6-10) in no particular order.\n\n"
            "Please enter your next 5 values, separated by commas:"
        )
        return NEXT_FIVE_VALUES
    
    # Parse values from text input
    values = parse_values(update.message.text)
    
    # Validate we have at least 1 value
    if not values:
        await update.message.reply_text(
            "⚠️ Please provide at least one value for positions 6-10."
        )
        return NEXT_FIVE_VALUES
    
    # Store up to 5 values
    next_values = values[:5]
    context.user_data['next_values'] = next_values
    
    # Continue to age collection
    await update.message.reply_text(
        f"Excellent! You've provided the following values for positions 6-10:\n"
        f"{format_values_for_display(next_values)}\n\n"
        f"Now, please enter your age:"
    )
    
    return AGE

async def collect_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collect age information from the user"""
    # Check if this is a callback query (edit request)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Let's update your age.\n\n"
            "Please enter your age:"
        )
        return AGE
    
    # Validate age
    is_valid, result = validate_age(update.message.text)
    
    if not is_valid:
        await update.message.reply_text(result)
        return AGE
    
    # Store age
    context.user_data['age'] = result
    
    # Continue to country collection
    await update.message.reply_text(
        f"Thank you. Now, please enter your country of residence:"
    )
    
    return COUNTRY

async def collect_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collect country information from the user"""
    # Check if this is a callback query (edit request)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Let's update your country of residence.\n\n"
            "Please enter your country:"
        )
        return COUNTRY
    
    # Validate country
    is_valid, result = validate_country(update.message.text)
    
    if not is_valid:
        await update.message.reply_text(result)
        return COUNTRY
    
    # Store country
    context.user_data['country'] = result
    
    # Continue to occupation collection
    await update.message.reply_text(
        f"Thank you. Finally, please enter your occupation:"
    )
    
    return OCCUPATION

async def collect_occupation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collect occupation information from the user"""
    # Check if this is a callback query (edit request)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Let's update your occupation.\n\n"
            "Please enter your occupation:"
        )
        return OCCUPATION
    
    # Validate occupation
    is_valid, result = validate_occupation(update.message.text)
    
    if not is_valid:
        await update.message.reply_text(result)
        return OCCUPATION
    
    # Store occupation
    context.user_data['occupation'] = result
    
    # Continue to review inputs
    await review_inputs(update, context)
    
    return REVIEW

async def review_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show a summary of collected data and ask for confirmation"""
    top_values = context.user_data.get('top_values', [])
    next_values = context.user_data.get('next_values', [])
    age = context.user_data.get('age', 'Not provided')
    country = context.user_data.get('country', 'Not provided')
    occupation = context.user_data.get('occupation', 'Not provided')
    
    # Create review message
    review_message = (
        "📋 Please review your information:\n\n"
        "Top 5 Values (ranked):\n"
    )
    
    # Add ranked values
    for i, value in enumerate(top_values[:5], 1):
        review_message += f"{i}. {value}\n"
    
    # Add next values
    review_message += f"\nValues 6-10:\n{format_values_for_display(next_values)}\n\n"
    
    # Add personal details
    review_message += (
        f"Age: {age}\n"
        f"Country: {country}\n"
        f"Occupation: {occupation}\n\n"
        f"Is this information correct? If yes, I'll generate your values report."
    )
    
    # Create inline keyboard for editing or confirming
    keyboard = [
        [
            InlineKeyboardButton("Edit Top 5 Values", callback_data="edit_top_five"),
            InlineKeyboardButton("Edit Next 5 Values", callback_data="edit_next_five")
        ],
        [
            InlineKeyboardButton("Edit Age", callback_data="edit_age"),
            InlineKeyboardButton("Edit Country", callback_data="edit_country"),
            InlineKeyboardButton("Edit Occupation", callback_data="edit_occupation")
        ],
        [InlineKeyboardButton("✅ Confirm and Generate Report", callback_data="confirm")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send or edit the message
    if update.callback_query:
        await update.callback_query.edit_message_text(review_message, reply_markup=reply_markup)
    else:
        await update.message.reply_text(review_message, reply_markup=reply_markup)
    
    return REVIEW

async def confirm_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle confirmation to generate the report"""
    query = update.callback_query
    await query.answer()
    
    # Inform user that report generation is starting
    await query.edit_message_text(
        "📊 Thank you for confirming your information!\n\n"
        "I'm now generating your personalised values report. This may take a minute or two...\n\n"
        "Please wait while I process your data and create your PDF report."
    )
    
    # Store user data in database
    user_id = update.effective_user.id
    success, record_id = store_user_data(user_id, context.user_data)
    
    if not success:
        await query.edit_message_text(
            "⚠️ There was an error storing your data. Please try again later or contact support."
        )
        return ConversationHandler.END
    
    # Generate report sections
    await generate_report(update, context)
    
    return GENERATING_REPORT

async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Generate the report using LLM and send PDF to user"""
    user_id = update.effective_user.id
    
    try:
        # Get user data
        user_data = context.user_data
        
        # Generate content for all sections
        sections_content, prompts_used = await generate_all_sections(user_data)
        
        # Store report data
        report_data = {
            'sections_content': sections_content,
            'prompts_used': prompts_used,
            'generation_date': 'now()'
        }
        store_report(user_id, report_data)
        
        # Generate PDF
        success, result = generate_pdf(user_data, sections_content)
        
        if not success:
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    f"⚠️ Error generating PDF: {result}"
                )
            else:
                await update.message.reply_text(
                    f"⚠️ Error generating PDF: {result}"
                )
            return ConversationHandler.END
        
        # Send PDF to user
        pdf_path = result
        
        # Message indicating report is ready
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "✅ Your Values report is ready!\n\n"
                "Here's what's included in your report:\n"
                "- What does this mean for me?\n"
                "- Are my values in parallel or in tension?\n"
                "- What do my values say about how I make decisions?\n"
                "- What do my values say about how I build relationships?\n\n"
                "I'm sending your PDF report now..."
            )
        else:
            await update.message.reply_text(
                "✅ Your Values report is ready!\n\n"
                "Here's what's included in your report:\n"
                "- What does this mean for me?\n"
                "- Are my values in parallel or in tension?\n"
                "- What do my values say about how I make decisions?\n"
                "- What do my values say about how I build relationships?\n\n"
                "I'm sending your PDF report now..."
            )
        
        # Send the PDF
        with open(pdf_path, 'rb') as file:
            await context.bot.send_document(
                chat_id=user_id,
                document=file,
                filename=f"Values_Report_{user_id}.pdf",
                caption="Here is your personalised Values report!"
            )
        
        # Cleanup the temporary PDF file
        cleanup_pdf(pdf_path)
        
        # Thank the user and end conversation
        await context.bot.send_message(
            chat_id=user_id,
            text="Thank you for using the Personal Values Report Bot! 🌟\n\n"
                "If you'd like to create another report, just type /start to begin again."
        )
        
        return ConversationHandler.END
    
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "⚠️ I encountered an error while generating your report. Please try again later."
            )
        else:
            await update.message.reply_text(
                "⚠️ I encountered an error while generating your report. Please try again later."
            )
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation"""
    await update.message.reply_text(
        "❌ Report generation canceled. Your data has not been saved.\n\n"
        "You can start again anytime by using the /start command."
    )
    context.user_data.clear()
    return ConversationHandler.END