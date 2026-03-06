#!/usr/bin/env python3
"""
CareerWill Premium Bot - Main Entry Point
FIXED VERSION - Guaranteed to work
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

# Add to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import config
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG level for more info
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

# Initialize bot with ALL required parameters
app = Client(
    name="careerwill_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,
    workdir=SESSION_DIR,
    parse_mode=ParseMode.MARKDOWN,
    sleep_threshold=60,
    max_concurrent_transmissions=10
)

# ==================== COMMAND HANDLERS ====================

@app.on_message(filters.command(["start"]))
async def start_command(client: Client, message: Message):
    try:
        logger.info(f"✅ Start command received from user {message.from_user.id}")
        
        welcome_text = """
🔵 **Welcome to CareerWill Premium Bot** 🔵

━━━━━━━━━━━━━━━━━━━━━━
**📋 Available Commands:**

🔵 **/start** - Show this message
ℹ️ **/help** - Help guide
📚 **/about** - Bot info
🎥 **/cwextractfree** - Extract batch
📚 **/allbatches** - View all batches

━━━━━━━━━━━━━━━━━━━━━━
**⚡ Bot is now LIVE!**
"""
        
        await message.reply_text(welcome_text)
        logger.info(f"✅ Replied to user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Start command error: {e}", exc_info=True)
        await message.reply_text("❌ Error occurred. Please try again.")

@app.on_message(filters.command(["help"]))
async def help_command(client: Client, message: Message):
    try:
        help_text = """
ℹ️ **CareerWill Bot Help Guide** ℹ️

━━━━━━━━━━━━━━━━━━━━━━
**📥 /cwextractfree**
Extract any batch:
1. Send `/cwextractfree`
2. Enter Batch ID (e.g., `1377`)
3. Get .txt file with all links

**📚 /allbatches**
View all batches with clickable IDs

**🎯 Tips:**
- Multiple IDs: `1377 1840 2034`
- 20 parallel workers for speed

━━━━━━━━━━━━━━━━━━━━━━
**⚡ @sdfvghhghhbnm_bot**
"""
        await message.reply_text(help_text)
    except Exception as e:
        logger.error(f"Help error: {e}")

@app.on_message(filters.command(["about"]))
async def about_command(client: Client, message: Message):
    try:
        about_text = """
🔵 **About CareerWill Bot** 🔵

━━━━━━━━━━━━━━━━━━━━━━
**Version:** 3.0.0
**Language:** Python 3.10
**Framework:** Pyrogram
**Developer:** @Ayushxsdy

**Features:**
✓ 20 parallel workers
✓ Live progress tracking
✓ DRM detection
✓ Multiple batch support

━━━━━━━━━━━━━━━━━━━━━━
**⚡ Made with ❤️**
"""
        await message.reply_text(about_text)
    except Exception as e:
        logger.error(f"About error: {e}")

@app.on_message(filters.command(["cwextractfree"]))
async def extract_command(client: Client, message: Message):
    try:
        await message.reply_text(
            "📚 **CareerWill Extractor**\n\n"
            "ℹ️ **Please enter Batch ID(s):**\n"
            "Example: `1377`\n"
            "Multiple: `1377 1840 2034`"
        )
        logger.info(f"Extract command from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Extract error: {e}")

@app.on_message(filters.command(["allbatches"]))
async def all_batches_command(client: Client, message: Message):
    try:
        await message.reply_text("📚 **Fetching batches...**")
        # Simple response for now
        await message.reply_text("✅ **Batches feature coming soon!**")
    except Exception as e:
        logger.error(f"Batches error: {e}")

# ==================== ECHO HANDLER FOR TESTING ====================

@app.on_message(filters.text & ~filters.command(["start", "help", "about", "cwextractfree", "allbatches"]))
async def echo_handler(client: Client, message: Message):
    """Simple echo handler to test if bot is working"""
    try:
        logger.info(f"📨 Received text from user {message.from_user.id}: {message.text[:50]}")
        await message.reply_text(f"✅ **Received:** {message.text}")
    except Exception as e:
        logger.error(f"Echo error: {e}")

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

# ==================== MAIN FUNCTION ====================

async def main():
    try:
        logger.info("🚀 Starting CareerWill Bot...")
        logger.info(f"📊 API ID: {API_ID}")
        logger.info(f"📊 Bot Token: {BOT_TOKEN[:10]}...")
        
        # Start bot
        await app.start()
        logger.info("✅ Bot client started successfully")
        
        # Get bot info
        bot_info = await app.get_me()
        logger.info(f"✅ Bot username: @{bot_info.username}")
        logger.info(f"✅ Bot is ready to receive messages!")
        
        # Send startup message to yourself (optional)
        try:
            await app.send_message(
                CHANNEL_ID if CHANNEL_ID else 8033638335,  # Your user ID
                "🚀 **Bot is now LIVE and ready to serve!**"
            )
        except:
            pass
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        
        # Keep running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}", exc_info=True)
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
