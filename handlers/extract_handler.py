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

async def extract_command(client, message: Message):
    status = await message.reply_text(
        f"{EMOJI['batch']} **CareerWill Extractor**\n\n"
        f"{EMOJI['info']} **Enter Batch ID:**\n"
        f"Example: `1377`\nMultiple: `1377 1840 2034`"
    )
    
    try:
        msg = await client.listen(chat_id=message.chat.id, timeout=120)
        if not msg or not msg.text:
            await status.edit(f"{EMOJI['error']} **Timeout!**")
            return
        
        batch_input = msg.text.strip()
        await msg.delete()
    except asyncio.TimeoutError:
        await status.edit(f"{EMOJI['error']} **Timeout!**")
        return
    
    batch_ids = batch_input.split() if " " in batch_input else [batch_input]
    await status.delete()
    
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
        
        def update(status_text):
            asyncio.create_task(progress.edit(status_text))
        
        stats = extract_batch(bid, update)
        
        if not stats:
            await progress.edit(f"{EMOJI['error']} **Failed**")
            continue
        
        filename = await save_to_file(stats.batch_name, bid, [i['line'] for i in stats.items])
        
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
        
        try:
            await client.send_document(CHANNEL_ID, filename, caption=f"New: {stats.batch_name[:50]}")
        except:
            pass
        
        await cleanup_file(filename)
        await progress.edit(f"{EMOJI['success']} **Batch {bid} completed!**")
