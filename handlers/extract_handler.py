"""
Extract command handler for CareerWill Bot
Complete fixed version with proper text handler
"""

import asyncio
import time
from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters
from utils.api_helper import extract_batch, validate_batch_id
from utils.file_helper import save_to_file, cleanup_file
from config import EMOJI, CHANNEL_ID
import logging

logger = logging.getLogger(__name__)

# Store user states for batch input
user_states = {}

# ==================== EXTRACT COMMAND ====================

async def extract_command(client, message: Message):
    """Handle /cwextractfree command"""
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
    user_states[user_id] = {
        "step": "waiting_for_batch",
        "status_msg_id": status_msg.id,
        "chat_id": message.chat.id
    }
    
    logger.info(f"User {user_id} started extraction")

# ==================== TEXT HANDLER FOR BATCH INPUT ====================

# This function will be called from main.py's text handler
async def handle_batch_input(client, message: Message, state):
    """Handle batch ID input from user"""
    user_id = message.from_user.id
    batch_input = message.text.strip()
    status_msg_id = state.get("status_msg_id")
    
    try:
        # Delete user's message
        await message.delete()
        
        # Get status message
        status = await client.get_messages(message.chat.id, status_msg_id)
        await status.delete()
    except Exception as e:
        logger.error(f"Error getting status message: {e}")
        status = await message.reply_text("Processing...")
    
    # Parse batch IDs
    batch_ids = batch_input.split() if " " in batch_input else [batch_input]
    
    for idx, bid in enumerate(batch_ids, 1):
        bid = bid.strip()
        if not bid:
            continue
        
        # Validate batch ID
        if not validate_batch_id(bid):
            await message.reply_text(f"{EMOJI['error']} **Invalid ID:** `{bid}`")
            continue
        
        # Start processing
        progress = await message.reply_text(
            f"{EMOJI['processing']} **Processing {idx}/{len(batch_ids)}:** `{bid}`"
        )
        
        # Progress update callback
        def update_progress(status_text):
            asyncio.create_task(progress.edit(status_text))
        
        # Extract batch
        stats = extract_batch(bid, update_progress)
        
        if not stats:
            await progress.edit(f"{EMOJI['error']} **Failed to extract batch**")
            continue
        
        # Save to file
        filename = await save_to_file(
            stats.batch_name, 
            bid, 
            [i['line'] for i in stats.items]
        )
        
        # Create caption
        caption = (
            f"{EMOJI['batch']} **Extraction Complete**\n\n"
            f"**ID:** `{bid}`\n"
            f"**Name:** {stats.batch_name[:50]}\n"
            f"**Total:** {stats.total_items}\n"
            f"**Videos:** {stats.videos} | **PDFs:** {stats.pdfs} | **DRM:** {stats.drm_count}\n"
            f"**Time:** {stats.time_taken:.2f}s\n\n"
            f"{EMOJI['completed']} **@sdfvghhghhbnm_bot**"
        )
        
        # Send file
        await message.reply_document(document=filename, caption=caption)
        
        # Send to log channel
        try:
            await client.send_document(
                CHANNEL_ID, 
                filename, 
                caption=f"New: {stats.batch_name[:50]}"
            )
        except Exception as e:
            logger.error(f"Log channel error: {e}")
        
        # Cleanup file
        await cleanup_file(filename)
        
        # Update progress message
        await progress.edit(f"{EMOJI['success']} **Batch {bid} completed!**")
    
    # Clear user state
    if user_id in user_states:
        del user_states[user_id]

# ==================== GET USER STATE ====================

def get_user_state(user_id):
    """Get user state"""
    return user_states.get(user_id)

def clear_user_state(user_id):
    """Clear user state"""
    if user_id in user_states:
        del user_states[user_id]
