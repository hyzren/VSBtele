import os
import logging
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, render_template
from threading import Thread

#This is to avoid circular imports
from responses import get_response
from dictionary_handler import get_word_definition

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Verify token loading
if TOKEN:
    logger.info("BOT_TOKEN loaded successfully")
else:
    logger.error("Failed to load BOT_TOKEN")
    raise ValueError("BOT_TOKEN not found in environment variables")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text('Greetings! I am a bot proudly serving Lord Verity. I respond to mentions, specific keywords, and can define words and slang at your request!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
I am Lord Verity's loyal servant. Here's how to use me:

• I respond to: @verityslavebot mentions, the word 'slave', and replies to my messages
• Use /define word [lang] for definitions (e.g., /define santuy id)
• Supported languages: en, es, fr, de, it, ru, ar, hi, ja, ko, pt, tr, id
• I know Gen Z slang and have special Indonesian slang support
    """
    await update.message.reply_text(help_text)

async def define_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /define command"""
    if not context.args:
        await update.message.reply_text(
            "Please provide a word to define. Usage: /define word [lang]\n"
            "Example: /define hola es\n\n"
            "I'll check Urban Dictionary, Google Translate, and Free Dictionary APIs to find the best definition!"
        )
        return

    # Check if language is specified (last argument)
    if len(context.args) >= 2 and len(context.args[-1]) == 2:
        word = ' '.join(context.args[:-1])
        lang = context.args[-1].lower()
    else:
        word = ' '.join(context.args)
        lang = 'en'  # Default to English

    logger.info(f"Definition requested for word: {word} in language: {lang}")

    # Show typing action while processing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    definition = get_word_definition(word, lang)
    if definition:
        await update.message.reply_text(definition)
    else:
        await update.message.reply_text(f"Sorry, I couldn't find a definition for '{word}' in any of my sources (Urban Dictionary, Google Translate, or Free Dictionary).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    message_text = update.message.text.lower()
    chat_type = update.message.chat.type

    # Log incoming message details
    logger.info(f"Received message in {chat_type}: {message_text}")

    # Only process messages from groups
    if chat_type not in ['group', 'supergroup']:
        logger.info("Ignoring message from non-group chat")
        return

    # Make sure we have a central tracking mechanism for all used responses
    if 'all_used_responses' not in context.chat_data:
        context.chat_data['all_used_responses'] = set()
    
    # Create a dictionary to track the last responses by type if it doesn't exist
    if 'last_response_by_type' not in context.chat_data:
        context.chat_data['last_response_by_type'] = {}
        
    # Track last 5 sent responses to ensure variety
    if 'recent_responses' not in context.chat_data:
        context.chat_data['recent_responses'] = []
        
    # Log current number of used responses for debugging
    logger.debug(f"Current number of used responses: {len(context.chat_data['all_used_responses'])}")
    
    # Check if message is a reply to the bot
    replied_to_message = update.message.reply_to_message
    if replied_to_message and replied_to_message.from_user.id == context.bot.id:
        logger.info("Detected reply to bot's message")
        
        response = get_response('reply', context.chat_data['all_used_responses'])
        
        # Add to used responses
        context.chat_data['all_used_responses'].add(response)
        
        # Keep track of recent responses (max 5)
        context.chat_data['recent_responses'].append(response)
        if len(context.chat_data['recent_responses']) > 5:
            context.chat_data['recent_responses'].pop(0)
            
        logger.info(f"Sending reply response: {response}")
        await update.message.reply_text(response)
        return

    # Check for mentions or keywords
    if '@verityslavebot' in message_text or 'slave' in message_text:
        trigger_type = 'mention' if '@verityslavebot' in message_text else 'keyword'
        logger.info(f"Detected {trigger_type} trigger")
        
        response = get_response(trigger_type, context.chat_data['all_used_responses'])
        
        # Add to used responses
        context.chat_data['all_used_responses'].add(response)
        
        # Keep track of recent responses (max 5)
        context.chat_data['recent_responses'].append(response)
        if len(context.chat_data['recent_responses']) > 5:
            context.chat_data['recent_responses'].pop(0)
            
        logger.info(f"Sending {trigger_type} response: {response}")
        await update.message.reply_text(response)
        return

    # If no specific trigger is detected, don't respond
    logger.info("No trigger detected, not responding")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f'Update {update} caused error {context.error}')

# Use the keep_alive module for uptime monitoring
from keep_alive import keep_alive


def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('define', define_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    # Start the keep-alive server in a separate thread
    keep_alive()

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()