#!/usr/bin/env python3
"""
CareerWill Premium Bot - Main Entry Point
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

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
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID

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
    workers=20
)

# ==================== COMMAND HANDLERS ====================

@app.on_message(filters.command(["start"]))
async def start(client: Client, message: Message):
    try:
        await start_command(client, message)
        logger.info(f"User {message.from_user.id} started bot")
    except Exception as e:
        logger.error(f"Start error: {e}")
        await message.reply_text("❌ Error occurred")

@app.on_message(filters.command(["help"]))
async def help(client: Client, message: Message):
    try:
        await help_command(client, message)
    except Exception as e:
        logger.error(f"Help error: {e}")
        await message.reply_text("❌ Error occurred")

@app.on_message(filters.command(["about"]))
async def about(client: Client, message: Message):
    try:
        await about_command(client, message)
    except Exception as e:
        logger.error(f"About error: {e}")
        await message.reply_text("❌ Error occurred")

@app.on_message(filters.command(["cwextractfree"]))
async def extract(client: Client, message: Message):
    try:
        await extract_command(client, message)
    except Exception as e:
        logger.error(f"Extract error: {e}")
        await message.reply_text("❌ Error occurred")

@app.on_message(filters.command(["allbatches"]))
async def all_batches(client: Client, message: Message):
    try:
        await all_batches_command(client, message)
    except Exception as e:
        logger.error(f"Batches error: {e}")
        await message.reply_text("❌ Error occurred")

# ==================== CALLBACK HANDLERS ====================

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    try:
        await batches_callback(client, callback_query)
    except Exception as e:
        logger.error(f"Callback error: {e}")
        await callback_query.answer("❌ Error", show_alert=True)

# ==================== START BOT ====================

if __name__ == "__main__":
    logger.info("🚀 Starting CareerWill Bot...")
    app.run()
