
#!/usr/bin/env python3
"""
CareerWill Bot - ULTIMATE FIX VERSION
Simplest possible bot that WILL work
"""

import os
import sys
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your credentials
API_ID = 21503125
API_HASH = "bab9855c442e9e4e87f413cb5b9dc3f9"
BOT_TOKEN = "8768725493:AAFDhnWucAWD9Tl9djbRtOr6v5bUUOFmCQY"

# Create temp directory for session
SESSION_DIR = "/tmp/bot_session"
os.makedirs(SESSION_DIR, exist_ok=True)

# Create the bot with minimal settings
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=SESSION_DIR,
    sleep_threshold=30
)

logger.info("✅ Bot created")

# ==================== COMMAND HANDLERS ====================

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    logger.info(f"✅ /start from user {user_id}")
    
    await message.reply_text(
        "🎉 **Bot is working perfectly!** 🎉\n\n"
        "You can now use:\n"
        "/help - Get help\n"
        "/about - About bot"
    )

@app.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    """Handle /help command"""
    await message.reply_text(
        "📚 **Help Menu**\n\n"
        "This bot is now fixed!"
    )

@app.on_message(filters.command("about"))
async def about_handler(client: Client, message: Message):
    """Handle /about command"""
    await message.reply_text(
        "🤖 **About Bot**\n\n"
        "Version: 1.0\n"
        "Status: ✅ Working"
    )

@app.on_message(filters.command("cwextractfree"))
async def extract_handler(client: Client, message: Message):
    """Handle extract command"""
    await message.reply_text(
        "📥 **Extract Feature**\n\n"
        "Coming soon! Please wait..."
    )

@app.on_message(filters.command("allbatches"))
async def batches_handler(client: Client, message: Message):
    """Handle batches command"""
    await message.reply_text(
        "📚 **All Batches**\n\n"
        "Coming soon! Please wait..."
    )

# Catch all other messages
@app.on_message(filters.text & ~filters.command(["start", "help", "about", "cwextractfree", "allbatches"]))
async def echo_handler(client: Client, message: Message):
    """Echo any text message"""
    await message.reply_text(f"You said: {message.text}")

# ==================== START BOT ====================

async def main():
    try:
        logger.info("🚀 Starting bot...")
        await app.start()
        
        # Get bot info
        me = await app.get_me()
        logger.info(f"✅ Bot started: @{me.username}")
        
        # Send ready message to yourself
        try:
            await app.send_message(
                8033638335,  # Your user ID
                "🚀 **Bot is ready!**\n\nSend /start to test."
            )
            logger.info("✅ Ready message sent")
        except Exception as e:
            logger.error(f"Could not send ready message: {e}")
        
        # Keep running
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
