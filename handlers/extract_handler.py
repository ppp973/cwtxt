"""
Extract command handler for CareerWill Bot
"""

import time
import asyncio
from datetime import datetime
from pyrogram.types import Message
from utils.api_helper import extract_batch, validate_batch_id
from utils.file_helper import save_to_file, cleanup_file
from config import PREMIUM_COLORS as pc, CHANNEL_ID
import logging

logger = logging.getLogger(__name__)

async def extract_command(client, message: Message):
    """Handle /cwextractfree command"""
    
    status_msg = await message.reply_text(
        f"{pc['batch']} **CareerWill Batch Extractor**\n\n"
        f"{pc['info']} **Please enter the Batch ID:**\n"
        f"Example: `1377`\nMultiple: `1377 1840 2034`"
    )
    
    try:
        input_msg = await client.listen(chat_id=message.chat.id, timeout=120)
        if not input_msg or not input_msg.text:
            await status_msg.edit(f"{pc['error']} **Timeout!**")
            return
        
        batch_input = input_msg.text.strip()
        await input_msg.delete()
    except asyncio.TimeoutError:
        await status_msg.edit(f"{pc['error']} **Timeout!**")
        return
    
    batch_ids = batch_input.split() if " " in batch_input else [batch_input]
    await status_msg.delete()
    
    for idx, batch_id in enumerate(batch_ids, 1):
        if not batch_id.strip():
            continue
        
        if not validate_batch_id(batch_id):
            await message.reply_text(f"{pc['error']} **Invalid Batch ID:** `{batch_id}`")
            continue
        
        progress = await message.reply_text(f"{pc['batch']} **Processing {idx}/{len(batch_ids)}:** `{batch_id}`")
        
        def update(status):
            asyncio.create_task(progress.edit(status))
        
        stats = extract_batch(batch_id, update)
        
        if not stats:
            await progress.edit(f"{pc['error']} **Extraction failed**")
            continue
        
        filename = await save_to_file(stats.batch_name, batch_id, [i['line'] for i in stats.items])
        
        caption = (
            f"{pc['batch']} **Extraction Complete**\n\n"
            f"**ID:** `{batch_id}`\n"
            f"**Name:** {stats.batch_name[:50]}\n"
            f"**Total:** {stats.total_items}\n"
            f"**Videos:** {stats.videos} | **PDFs:** {stats.pdfs} | **DRM:** {stats.drm_count}\n"
            f"**Time:** {stats.time_taken:.2f}s"
        )
        
        await message.reply_document(document=filename, caption=caption)
        
        try:
            await client.send_document(CHANNEL_ID, filename, caption=f"New: {stats.batch_name[:50]}")
        except:
            pass
        
        await cleanup_file(filename)
        await progress.edit(f"{pc['success']} **Batch {batch_id} completed!**")
