import asyncio
import time
from pyrogram.types import Message
from utils.api_helper import extract_batch, validate_batch_id
from utils.file_helper import save_to_file, cleanup_file
from config import EMOJI, CHANNEL_ID
import logging

logger = logging.getLogger(__name__)

# Store user states
user_states = {}

async def extract_command(client, message: Message):
    user_id = message.from_user.id
    
    status_msg = await message.reply_text(
        f"{EMOJI['batch']} **CareerWill Extractor**\n\n"
        f"{EMOJI['info']} **Please enter Batch ID(s):**\n"
        f"Example: `1377`\n"
        f"Multiple: `1377 1840 2034`"
    )
    
    user_states[user_id] = {
        "step": "waiting_for_batch",
        "status_msg_id": status_msg.id,
        "chat_id": message.chat.id
    }

async def handle_batch_input(client, message: Message, state):
    user_id = message.from_user.id
    batch_input = message.text.strip()
    status_msg_id = state.get("status_msg_id")
    
    try:
        await message.delete()
        status = await client.get_messages(message.chat.id, status_msg_id)
        await status.delete()
    except:
        status = await message.reply_text("Processing...")
    
    batch_ids = batch_input.split() if " " in batch_input else [batch_input]
    
    for idx, bid in enumerate(batch_ids, 1):
        bid = bid.strip()
        if not bid:
            continue
        
        if not validate_batch_id(bid):
            await message.reply_text(f"{EMOJI['error']} **Invalid ID:** `{bid}`")
            continue
        
        progress = await message.reply_text(
            f"{EMOJI['processing']} **Processing {idx}/{len(batch_ids)}:** `{bid}`"
        )
        
        def update_progress(status_text):
            asyncio.create_task(progress.edit(status_text))
        
        stats = extract_batch(bid, update_progress)
        
        if not stats:
            await progress.edit(f"{EMOJI['error']} **Failed**")
            continue
        
        filename = await save_to_file(
            stats.batch_name, 
            bid, 
            [i['line'] for i in stats.items]
        )
        
        caption = (
            f"{EMOJI['batch']} **Extraction Complete**\n\n"
            f"**ID:** `{bid}`\n"
            f"**Name:** {stats.batch_name[:50]}\n"
            f"**Total:** {stats.total_items}\n"
            f"**Videos:** {stats.videos} | **PDFs:** {stats.pdfs} | **DRM:** {stats.drm_count}\n"
            f"**Time:** {stats.time_taken:.2f}s\n\n"
            f"{EMOJI['completed']} **@sdfvghhghhbnm_bot**"
        )
        
        await message.reply_document(document=filename, caption=caption)
        
        if CHANNEL_ID:
            try:
                await client.send_document(
                    CHANNEL_ID, 
                    filename, 
                    caption=f"New: {stats.batch_name[:50]}"
                )
            except:
                pass
        
        await cleanup_file(filename)
        await progress.edit(f"{EMOJI['success']} **Batch {bid} completed!**")
    
    if user_id in user_states:
        del user_states[user_id]

def get_user_state(user_id):
    return user_states.get(user_id)

def clear_user_state(user_id):
    if user_id in user_states:
        del user_states[user_id]
