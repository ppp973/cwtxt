from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.api_helper import get_all_batches
from config import PREMIUM_COLORS as pc
import logging

logger = logging.getLogger(__name__)

async def all_batches_command(client, message: Message):
    """Handle /allbatches command with premium UI"""
    
    status_msg = await message.reply_text(f"{pc['info']} **Fetching all batches...**")
    
    try:
        # Get all batches from API
        batches_data = get_all_batches()
        
        if not batches_data:
            await status_msg.edit(f"{pc['error']} **Failed to fetch batches. API might be down.**")
            return
        
        # Format batches for display
        batch_list = []
        batch_ids = []
        
        for batch_id, batch_name in batches_data.items():
            batch_list.append(f"`{batch_id}` - **{batch_name}**")
            batch_ids.append(batch_id)
        
        # Pagination (20 batches per page)
        items_per_page = 20
        total_pages = (len(batch_list) + items_per_page - 1) // items_per_page
        
        # Store in user session (you might want to use a proper session store)
        if not hasattr(message.chat, "batch_data"):
            message.chat.batch_data = {}
        
        message.chat.batch_data["all_batches"] = batches_data
        message.chat.batch_data["batch_ids"] = batch_ids
        message.chat.batch_data["current_page"] = 1
        message.chat.batch_data["total_pages"] = total_pages
        
        # Show first page
        await show_batches_page(message, status_msg, 1)
        
    except Exception as e:
        logger.error(f"Batches error: {str(e)}")
        await status_msg.edit(f"{pc['error']} **Error:** `{str(e)[:100]}`")

async def show_batches_page(message, status_msg, page):
    """Show paginated batches list"""
    
    batches_data = message.chat.batch_data["all_batches"]
    batch_ids = message.chat.batch_data["batch_ids"]
    total_pages = message.chat.batch_data["total_pages"]
    
    items_per_page = 20
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(batch_ids))
    
    # Build batch list for current page
    batch_text = f"{pc['batch']} **Available Batches - Page {page}/{total_pages}** {pc['batch']}\n\n"
    batch_text += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i in range(start_idx, end_idx):
        batch_id = batch_ids[i]
        batch_name = batches_data[batch_id]
        
        # Truncate long names
        if len(batch_name) > 50:
            batch_name = batch_name[:47] + "..."
        
        batch_text += f"`{batch_id}` ─ **{batch_name}**\n"
        
        # Add separator every 5 items
        if (i - start_idx + 1) % 5 == 0 and i < end_idx - 1:
            batch_text += "───────────────\n"
    
    batch_text += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    batch_text += f"\n{pc['info']} **Total Batches:** `{len(batch_ids)}`\n"
    batch_text += f"{pc['video']} **Click on any ID to copy**\n"
    
    # Create navigation buttons
    keyboard_buttons = []
    
    # First row: Batch IDs as buttons (first 5 of current page)
    row_buttons = []
    for i in range(start_idx, min(start_idx + 5, end_idx)):
        batch_id = batch_ids[i]
        row_buttons.append(InlineKeyboardButton(
            batch_id, 
            callback_data=f"copy_{batch_id}"
        ))
    if row_buttons:
        keyboard_buttons.append(row_buttons)
    
    # Second row: Next 5 batch IDs
    if end_idx - start_idx > 5:
        row_buttons = []
        for i in range(start_idx + 5, end_idx):
            batch_id = batch_ids[i]
            row_buttons.append(InlineKeyboardButton(
                batch_id, 
                callback_data=f"copy_{batch_id}"
            ))
        if row_buttons:
            keyboard_buttons.append(row_buttons)
    
    # Navigation row
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("◀️ Prev", callback_data=f"page_{page-1}"))
    
    nav_buttons.append(InlineKeyboardButton(f"📊 {page}/{total_pages}", callback_data="current"))
    
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"page_{page+1}"))
    
    keyboard_buttons.append(nav_buttons)
    
    # Action row
    action_buttons = [
        InlineKeyboardButton("📥 Extract", callback_data="go_extract"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh_batches")
    ]
    keyboard_buttons.append(action_buttons)
    
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    await status_msg.edit(batch_text, reply_markup=keyboard)

# Callback handlers
async def batches_callback(client, callback_query):
    """Handle batch-related callbacks"""
    data = callback_query.data
    
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await show_batches_page(
            callback_query.message,
            callback_query.message,
            page
        )
        await callback_query.answer()
        
    elif data.startswith("copy_"):
        batch_id = data.split("_")[1]
        await callback_query.answer(f"✅ Batch ID {batch_id} copied!", show_alert=True)
        
    elif data == "go_extract":
        await callback_query.message.delete()
        from handlers.extract_handler import extract_command
        await extract_command(client, callback_query.message)
        
    elif data == "refresh_batches":
        await callback_query.message.edit(f"{pc['info']} **Refreshing...**")
        await all_batches_command(client, callback_query.message)
