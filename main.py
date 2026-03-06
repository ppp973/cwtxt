#!/usr/bin/env python3
"""
CareerWill Bot - DEBUG VERSION
This version logs EVERYTHING to find the issue
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
from pyrogram.enums import ParseMode
from pyrogram.errors import *

# Configure logging to be VERY verbose
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG level shows everything
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Set pyrogram logging to DEBUG
logging.getLogger("pyrogram").setLevel(logging.DEBUG)
logging.getLogger("pyrogram.client").setLevel(logging.DEBUG)
logging.getLogger("pyrogram.session").setLevel(logging.DEBUG)
logging.getLogger("pyrogram.connection").setLevel(logging.DEBUG)

logger.info("=" * 60)
logger.info("🚀 BOT STARTING IN DEBUG MODE")
logger.info("=" * 60)

# Configuration
API_ID = 21503125
API_HASH = "bab9855c442e9e4e87f413cb5b9dc3f9"
BOT_TOKEN = "8768725493:AAFDhnWucAWD9Tl9djbRtOr6v5bUUOFmCQY"

logger.info(f"📊 API ID: {API_ID}")
logger.info(f"📊 Bot Token: {BOT_TOKEN[:10]}...")

# Create directories
DOWNLOAD_DIR = "downloads"
SESSION_DIR = "/tmp/careerwill_sessions"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(SESSION_DIR, exist_ok=True)
os.chmod(DOWNLOAD_DIR, 0o777)
os.chmod(SESSION_DIR, 0o777)

logger.info(f"📁 Download dir: {DOWNLOAD_DIR}")
logger.info(f"📁 Session dir: {SESSION_DIR}")

# Initialize bot
app = Client(
    name="careerwill_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,
    workdir=SESSION_DIR,
    parse_mode=ParseMode.MARKDOWN
)

logger.info("✅ Bot client created")

# ==================== COMMAND HANDLERS ====================

@app.on_message(filters.command(["start"]))
async def start_command(client: Client, message: Message):
    """START command handler"""
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        logger.info(f"✅ START command received from user {user_id} ({user_name})")
        logger.info(f"📨 Message details: {message}")
        
        response = "🎉 **Bot is working!** 🎉\n\nYou sent /start command"
        await message.reply_text(response)
        logger.info(f"✅ Replied to user {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Error in start_command: {e}", exc_info=True)

@app.on_message(filters.command(["help"]))
async def help_command(client: Client, message: Message):
    """HELP command handler"""
    try:
        user_id = message.from_user.id
        logger.info(f"✅ HELP command from user {user_id}")
        await message.reply_text("Help command received! Bot is working.")
    except Exception as e:
        logger.error(f"❌ Help error: {e}")

@app.on_message(filters.command(["about"]))
async def about_command(client: Client, message: Message):
    """ABOUT command handler"""
    try:
        user_id = message.from_user.id
        logger.info(f"✅ ABOUT command from user {user_id}")
        await message.reply_text("About command received! Bot is working.")
    except Exception as e:
        logger.error(f"❌ About error: {e}")

@app.on_message(filters.command(["cwextractfree"]))
async def extract_command(client: Client, message: Message):
    """EXTRACT command handler"""
    try:
        user_id = message.from_user.id
        logger.info(f"✅ EXTRACT command from user {user_id}")
        await message.reply_text("Extract command received! Bot is working.")
    except Exception as e:
        logger.error(f"❌ Extract error: {e}")

@app.on_message(filters.command(["allbatches"]))
async def batches_command(client: Client, message: Message):
    """BATCHES command handler"""
    try:
        user_id = message.from_user.id
        logger.info(f"✅ BATCHES command from user {user_id}")
        await message.reply_text("Batches command received! Bot is working.")
    except Exception as e:
        logger.error(f"❌ Batches error: {e}")

# ==================== CATCH ALL HANDLER ====================

@app.on_message()
async def catch_all(client: Client, message: Message):
    """Catch ALL messages (for debugging)"""
    try:
        user_id = message.from_user.id
        text = message.text if message.text else "[NO TEXT]"
        logger.info(f"📨 GOT MESSAGE from user {user_id}: {text}")
        
        # Always reply to any message
        await message.reply_text(f"✅ **Message received!**\n\nYou said: {text}")
        logger.info(f"✅ Replied to user {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Error in catch_all: {e}", exc_info=True)

# ==================== HEALTH CHECK SERVER ====================

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')
    
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"✅ Health check server on port {port}")
    server.serve_forever()

# ==================== MAIN FUNCTION ====================

async def main():
    try:
        logger.info("=" * 60)
        logger.info("🚀 STARTING BOT...")
        logger.info("=" * 60)
        
        # Start bot
        logger.info("⏳ Calling app.start()...")
        await app.start()
        logger.info("✅ app.start() completed")
        
        # Get bot info
        logger.info("⏳ Getting bot info...")
        bot_info = await app.get_me()
        logger.info(f"✅ Bot info retrieved: @{bot_info.username} (ID: {bot_info.id})")
        
        # Send startup message
        try:
            logger.info("⏳ Sending startup message...")
            await app.send_message(
                chat_id=8033638335,  # Your user ID
                text="🚀 **Bot is now LIVE and ready to serve!**"
            )
            logger.info("✅ Startup message sent")
        except Exception as e:
            logger.error(f"❌ Could not send startup message: {e}")
        
        logger.info("=" * 60)
        logger.info("✅ BOT IS RUNNING AND READY TO RECEIVE MESSAGES!")
        logger.info("=" * 60)
        
        # Keep running
        while True:
            await asyncio.sleep(1)
        
    except Exception as e:
        logger.error(f"❌ FATAL ERROR: {e}", exc_info=True)
        raise
    finally:
        logger.info("🛑 Stopping bot...")
        await app.stop()
        logger.info("✅ Bot stopped")

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    try:
        # Start health check server
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        
        # Run the bot
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
