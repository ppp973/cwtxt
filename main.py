#!/usr/bin/env python3
"""
CareerWill Premium Bot - Main Entry Point
Telegram Bot for extracting CareerWill course content
COMPLETE FINAL VERSION - All errors fixed
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Add to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import config
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID, EMOJI

# Import handlers
from handlers.start_handler import start_command
from handlers.help_handler import help_command
from handlers.about_handler import about_command
from handlers.batches_handler import all_batches_command, batches_callback

# Import extract handler functions
from handlers.extract_handler import (
    extract_command,
    get_user_state,
    handle_batch_input,
    clear_user_state
)

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
        await extract_command(client, message)
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
        
        # Get user state
        state = get_user_state(user_id)
        
        # Check if user is waiting for batch input
        if state and state.get("step") == "waiting_for_batch":
            logger.info(f"Processing batch input from user {user_id}")
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
        logger.info("Startup notification sent to channel")
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
        logger.info("✅ Bot client started successfully")
        
        # Send startup notification
        await send_startup_notification()
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        
        # Keep running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        logger.info("🛑 Stopping bot...")
        await app.stop()
        logger.info("✅ Bot stopped")

# ==================== HEALTH CHECK ENDPOINT (for Render) ====================

# This is a simple HTTP server to keep Render happy
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot is running!')
    
    def log_message(self, format, *args):
        # Suppress log messages
        pass

def run_health_server():
    """Run a simple HTTP server for health checks"""
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    try:
        # Start health check server in a separate thread
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        
        # Run the bot
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
