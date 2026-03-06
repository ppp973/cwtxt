#!/usr/bin/env python3
"""
CareerWill Premium Bot - Main Entry Point
COMPLETE WORKING VERSION - All errors fixed
"""

import os
import sys
import logging
import asyncio
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, filters
from pyrogram.types import Message

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

# Create necessary directories
DOWNLOAD_DIR = "downloads"
SESSION_DIR = "/tmp/careerwill_sessions"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(SESSION_DIR, exist_ok=True)

os.chmod(DOWNLOAD_DIR, 0o777)
os.chmod(SESSION_DIR, 0o777)

logger.info(f"📁 Download directory: {os.path.abspath(DOWNLOAD_DIR)}")
logger.info(f"📁 Session directory: {SESSION_DIR}")

# Initialize bot
app = Client(
    "careerwill_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,
    workdir=SESSION_DIR
)

# ==================== COMMAND HANDLERS ====================

@app.on_message(filters.command(["start"]))
async def start(client: Client, message: Message):
    try:
        await start_command(client, message)
        logger.info(f"User {message.from_user.id} started bot")
    except Exception as e:
        logger.error(f"Start error: {e}")
        await message.reply_text(f"{EMOJI['error']} Error occurred")

@app.on_message(filters.command(["help"]))
async def help(client: Client, message: Message):
    try:
        await help_command(client, message)
    except Exception as e:
        logger.error(f"Help error: {e}")
        await message.reply_text(f"{EMOJI['error']} Error occurred")

@app.on_message(filters.command(["about"]))
async def about(client: Client, message: Message):
    try:
        await about_command(client, message)
    except Exception as e:
        logger.error(f"About error: {e}")
        await message.reply_text(f"{EMOJI['error']} Error occurred")

@app.on_message(filters.command(["cwextractfree"]))
async def extract(client: Client, message: Message):
    try:
        await extract_command(client, message)
    except Exception as e:
        logger.error(f"Extract error: {e}")
        await message.reply_text(f"{EMOJI['error']} Error occurred")

@app.on_message(filters.command(["allbatches"]))
async def all_batches(client: Client, message: Message):
    try:
        await all_batches_command(client, message)
    except Exception as e:
        logger.error(f"Batches error: {e}")
        await message.reply_text(f"{EMOJI['error']} Error occurred")

# ==================== TEXT HANDLER ====================

@app.on_message(filters.text & ~filters.command(["start", "help", "about", "cwextractfree", "allbatches"]))
async def text_handler(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        state = get_user_state(user_id)
        
        if state and state.get("step") == "waiting_for_batch":
            logger.info(f"Processing batch input from user {user_id}")
            await handle_batch_input(client, message, state)
            clear_user_state(user_id)
            
    except Exception as e:
        logger.error(f"Text handler error: {e}")
        clear_user_state(message.from_user.id)

# ==================== CALLBACK HANDLER ====================

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    try:
        await batches_callback(client, callback_query)
    except Exception as e:
        logger.error(f"Callback error: {e}")
        await callback_query.answer(f"{EMOJI['error']} Error", show_alert=True)

# ==================== HEALTH CHECK SERVER ====================

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'CareerWill Bot is running! Status: Online')
    
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"✅ Health check server running on port {port}")
    server.serve_forever()

# ==================== STARTUP NOTIFICATION ====================

async def send_startup_notification():
    if CHANNEL_ID:
        try:
            await app.send_message(
                CHANNEL_ID,
                f"{EMOJI['success']} **Bot Started!**\n\n"
                f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"**Status:** ✅ Online\n"
                f"**Version:** 3.0.0"
            )
            logger.info("Startup notification sent")
        except Exception as e:
            logger.error(f"Startup notification error: {e}")
    else:
        logger.info("No channel ID - skipping notification")

# ==================== MAIN FUNCTION ====================

async def main():
    try:
        logger.info("🚀 Starting CareerWill Bot...")
        
        await app.start()
        logger.info("✅ Bot client started successfully")
        
        await send_startup_notification()
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        logger.info("🛑 Stopping bot...")
        await app.stop()
        logger.info("✅ Bot stopped")

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    try:
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
