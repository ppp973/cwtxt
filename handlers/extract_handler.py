import asyncio
import time
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from utils.api_helper import extract_batch
from utils.file_helper import save_to_file, cleanup_file
from config import PREMIUM_COLORS as pc, CHANNEL_ID
import logging

logger = logging.getLogger(__name__)

async def extract_command(client, message: Message):
    """Handle /cwextractfree command"""
    
    status_msg = await message.reply_text(
        f"{pc['batch']} **CareerWill Batch Extractor** {pc['batch']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{pc['info']} **Please enter the Batch ID:**\n\n"
        f"**Example:** `1377`\n"
        f"**Multiple:** `1377 1840 2034`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    # Get batch ID from user
    input_msg = await client.listen(chat_id=message.chat.id, timeout=120)
    
    if not input_msg or not input_msg.text:
        await status_msg.edit(f"{pc['error']} **Timeout! Please try again.**")
        return
    
    batch_input = input_msg.text.strip()
    await input_msg.delete()
    
    # Parse batch IDs
    if " " in batch_input:
        batch_ids = batch_input.split()
    else:
        batch_ids = [batch_input]
    
    await status_msg.delete()
    
    # Process each batch
    for batch_id in batch_ids:
        batch_id = batch_id.strip()
        if not batch_id:
            continue
        
        # Start extraction
        progress_msg = await message.reply_text(
            f"{pc['batch']} **Batch ID:** `{batch_id}`\n"
            f"{pc['info']} **Status:** Initializing...\n"
            f"{pc['time']} **Started:** {datetime.now().strftime('%H:%M:%S')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        # Progress callback
        last_update = time.time()
        progress_text = ""
        
        def update_progress(status):
            nonlocal last_update, progress_text
            current_time = time.time()
            
            # Update every 2 seconds
            if current_time - last_update > 2:
                progress_text = status
                last_update = current_time
        
        try:
            # Extract batch
            result = extract_batch(batch_id, update_progress)
            
            if not result:
                await progress_msg.edit(
                    f"{pc['error']} **Extraction Failed**\n\n"
                    f"**Batch ID:** `{batch_id}`\n"
                    f"**Reason:** Invalid batch ID or API error\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━"
                )
                continue
            
            # Show progress updates
            await progress_msg.edit(
                f"{pc['batch']} **Batch:** `{result['batch_name'][:50]}`\n"
                f"{pc['stats']} **Found:** {result['total']} items\n"
                f"{pc['video']} **Videos:** {result['videos']}\n"
                f"{pc['pdf']} **PDFs:** {result['pdfs']}\n"
                f"{pc['time']} **Time:** {result['time']}s\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{pc['success']} **Saving file...**"
            )
            
            # Save to file
            filename = await save_to_file(
                result['batch_name'],
                batch_id,
                result['items']
            )
            
            if not filename:
                await progress_msg.edit(
                    f"{pc['error']} **File Save Failed**\n\n"
                    f"**Batch:** {result['batch_name'][:50]}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━"
                )
                continue
            
            # Create caption
            end_time = datetime.now()
            caption = (
                f"{pc['batch']} **CareerWill Extraction Complete** {pc['batch']}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"**📋 Batch Details:**\n"
                f"├ ID: `{batch_id}`\n"
                f"├ Name: {result['batch_name'][:50]}\n"
                f"└ Total Items: {result['total']}\n\n"
                f"**📊 Statistics:**\n"
                f"├ {pc['video']} Videos: {result['videos']}\n"
                f"├ {pc['pdf']} PDFs: {result['pdfs']}\n"
                f"├ {pc['drm']} DRM: {result.get('drm', 0)}\n"
                f"└ {pc['time']} Time: {result['time']}s\n\n"
                f"**⚡ Extracted by @sdfvghhghhbnm_bot**\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━"
            )
            
            # Send file
            await message.reply_document(
                document=filename,
                caption=caption
            )
            
            # Send to log channel
            try:
                await client.send_document(
                    CHANNEL_ID,
                    filename,
                    caption=f"**New Extraction:** {result['batch_name'][:50]}\n**Batch ID:** {batch_id}"
                )
            except:
                pass
            
            # Cleanup
            await cleanup_file(filename)
            
            # Success message
            await progress_msg.edit(
                f"{pc['success']} **Extraction Successful!** {pc['success']}\n\n"
                f"**Batch:** {result['batch_name'][:50]}\n"
                f"**Items:** {result['total']}\n"
                f"**Time:** {result['time']}s\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{pc['info']} **File has been sent above!**"
            )
            
        except Exception as e:
            logger.error(f"Extraction error: {str(e)}")
            await progress_msg.edit(
                f"{pc['error']} **Extraction Error**\n\n"
                f"**Batch ID:** `{batch_id}`\n"
                f"**Error:** `{str(e)[:100]}`\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{pc['info']} **Please try again later.**"
            )
    
    # Final message if multiple batches
    if len(batch_ids) > 1:
        await message.reply_text(
            f"{pc['success']} **All batches processed!** {pc['success']}\n\n"
            f"**Total Batches:** {len(batch_ids)}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
