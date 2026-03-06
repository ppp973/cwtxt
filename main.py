#!/usr/bin/env python3
"""
CareerWill Premium Bot - Main Entry Point
Telegram Bot for extracting CareerWill course content
Fully fixed version with proper text handling and no 'listen' attribute errors
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

# Add to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import handlers
from handlers import (
    start_command,
    help_command,
    about_command,
    extract_command,
    all_batches_command,
    batches_callback
)

# Import text handler from extract_handler
from handlers.extract_handler import handle_batch_input

# Import config
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID, EMOJI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create downloads directory
os.makedirs("downloads", exist_ok=True)

# Initialize bot
app = Client(
    "careerwill_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,
    workdir="./sessions"
)

# ==================== USER STATE MANAGEMENT ====================

# Store user states for batch input
user_states = {}

def get_user_state(user_id):
    """Get user state"""
    return user_states.get(user_id, {})

def set_user_state(user_id, state):
    """Set user state"""
    user_states[user_id] = state

def clear_user_state(user_id):
    """Clear user state"""
    if user_id in user_states:
        del user_states[user_id]

# ==================== COMMAND HANDLERS ====================

@app.on_message(filters.command(["start"]))
async def start(client: Client, message: Message):
    """Handle /start command"""
    try:
        await start_command(client, message)
        logger.info(f"User {message.from_user.id} started bot")
    except Exception as e:
        logger.error(f"Start error: {e}")
        await message.reply_text(f"{EMOJI['error']} **Error occurred**")

@app.on_message(filters.command(["help"]))
async def help(client: Client, message: Message):
    """Handle /help command"""
    try:
        await help_command(client, message)
    except Exception as e:
        logger.error(f"Help error: {e}")
        await message.reply_text(f"{EMOJI['error']} **Error occurred**")

@app.on_message(filters.command(["about"]))
async def about(client: Client, message: Message):
    """Handle /about command"""
    try:
        await about_command(client, message)
    except Exception as e:
        logger.error(f"About error: {e}")
        await message.reply_text(f"{EMOJI['error']} **Error occurred**")

@app.on_message(filters.command(["cwextractfree"]))
async def extract(client: Client, message: Message):
    """Handle /cwextractfree command"""
    try:
        user_id = message.from_user.id
        
        # Set user state to waiting for batch input
        status_msg = await message.reply_text(
            f"{EMOJI['batch']} **CareerWill Extractor**\n\n"
            f"{EMOJI['info']} **Please enter Batch ID(s):**\n"
            f"Example: `1377`\n"
            f"Multiple: `1377 1840 2034`\n\n"
            f"{EMOJI['time']} *You have 2 minutes*"
        )
        
        # Store user state
        set_user_state(user_id, {
            "step": "waiting_for_batch",
            "status_msg_id": status_msg.id,
            "chat_id": message.chat.id
        })
        
        logger.info(f"User {user_id} started extraction")
        
    except Exception as e:
        logger.error(f"Extract error: {e}")
        await message.reply_text(f"{EMOJI['error']} **Error occurred**")

@app.on_message(filters.command(["allbatches"]))
async def all_batches(client: Client, message: Message):
    """Handle /allbatches command"""
    try:
        await all_batches_command(client, message)
    except Exception as e:
        logger.error(f"Batches error: {e}")
        await message.reply_text(f"{EMOJI['error']} **Error occurred**")

# ==================== TEXT HANDLER FOR BATCH INPUT ====================

@app.on_message(filters.text & ~filters.command(["start", "help", "about", "cwextractfree", "allbatches"]))
async def text_handler(client: Client, message: Message):
    """Handle text messages (for batch input)"""
    try:
        user_id = message.from_user.id
        state = get_user_state(user_id)
        
        # Check if user is waiting for batch input
        if state.get("step") == "waiting_for_batch":
            await handle_batch_input(client, message, state)
            clear_user_state(user_id)
        else:
            # Ignore other text messages
            pass
            
    except Exception as e:
        logger.error(f"Text handler error: {e}")
        clear_user_state(message.from_user.id)

# ==================== CALLBACK HANDLERS ====================

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    """Handle all callback queries"""
    try:
        await batches_callback(client, callback_query)
    except Exception as e:
        logger.error(f"Callback error: {e}")
        await callback_query.answer(f"{EMOJI['error']} Error", show_alert=True)

# ==================== ERROR HANDLER ====================

@app.on_message()
async def error_handler(client: Client, message: Message):
    """Handle unknown commands"""
    if not message.text:
        return
        
    if message.text.startswith('/'):
        await message.reply_text(
            f"{EMOJI['error']} **Unknown Command**\n\n"
            f"Use /start to see available commands."
        )

# ==================== STARTUP NOTIFICATION ====================

async def send_startup_notification():
    """Send startup notification to log channel"""
    try:
        await app.send_message(
            CHANNEL_ID,
            f"{EMOJI['success']} **Bot Started!**\n\n"
            f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Status:** ✅ Online\n"
            f"**Workers:** 20\n"
            f"**Version:** 3.0.0"
        )
    except Exception as e:
        logger.error(f"Startup notification error: {e}")

# ==================== MAIN FUNCTION ====================

async def main():
    """Main function"""
    try:
        logger.info("🚀 Starting CareerWill Bot...")
        logger.info(f"📊 API ID: {API_ID}")
        logger.info(f"📊 Bot Token: {BOT_TOKEN[:10]}...")
        logger.info(f"📊 Channel ID: {CHANNEL_ID}")
        
        # Start bot
        await app.start()
        
        # Send startup notification
        await send_startup_notification()
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        
        # Keep running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        await app.stop()

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
