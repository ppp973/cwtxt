import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

# Import handlers
from handlers.start_handler import start_command
from handlers.help_handler import help_command
from handlers.about_handler import about_command
from handlers.extract_handler import extract_command
from handlers.batches_handler import all_batches_command, batches_callback

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create downloads directory
os.makedirs("downloads", exist_ok=True)

# Initialize bot
app = Client(
    "careerwill_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Command handlers
@app.on_message(filters.command(["start"]))
async def start(client, message):
    await start_command(client, message)

@app.on_message(filters.command(["help"]))
async def help(client, message):
    await help_command(client, message)

@app.on_message(filters.command(["about"]))
async def about(client, message):
    await about_command(client, message)

@app.on_message(filters.command(["cwextractfree"]))
async def extract(client, message):
    await extract_command(client, message)

@app.on_message(filters.command(["allbatches"]))
async def all_batches(client, message):
    await all_batches_command(client, message)

# Callback query handler
@app.on_callback_query()
async def handle_callback(client, callback_query):
    await batches_callback(client, callback_query)

# Error handler
@app.on_message()
async def error_handler(client, message):
    if not message.text.startswith('/'):
        await message.reply_text(
            "**❌ Unknown Command**\n\n"
            "Use /start to see available commands."
        )

if __name__ == "__main__":
    logger.info("🚀 CareerWill Premium Bot Started!")
    app.run()
