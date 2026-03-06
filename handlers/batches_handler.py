from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.api_helper import get_all_batches
from config import EMOJI
import logging

logger = logging.getLogger(__name__)
user_sessions = {}

async def all_batches_command(client, message: Message):
    status = await message.reply_text(f"{EMOJI['info']} **Fetching batches...**")
    
    batches = get_all_batches()
    if not batches:
        await status.edit(f"{EMOJI['error']} **Failed to fetch batches**")
        return
    
    sorted_batches = dict(sorted(batches.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0]))
    
    uid = message.from_user.id
    user_sessions[uid] = {
        "batches": sorted_batches,
        "ids": list(sorted_batches.keys()),
        "page": 1,
        "per_page": 15
    }
    
    await show_page(message, status, uid, 1)

async def show_page(client, msg, uid, page):
    session = user_sessions.get(uid)
    if not session:
        return
    
    batches = session["batches"]
    ids = session["ids"]
    per_page = session["per_page"]
    total = len(ids)
    pages = (total + per_page - 1) // per_page
    page = max(1, min(page, pages))
    session["page"] = page
    
    start = (page - 1) * per_page
    end = min(start + per_page, total)
    
    text = f"{EMOJI['batch']} **Batches - Page {page}/{pages}** {EMOJI['batch']}\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i in range(start, end):
        bid = ids[i]
        name = batches[bid]
        if len(name) > 40:
            name = name[:37] + "..."
        text += f"`{bid}` ─ **{name}**\n"
    
    text += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"\n{EMOJI['info']} **Total:** {total} | Click IDs to copy"
    
    buttons = []
    
    row = []
    for i in range(start, min(start + 5, end)):
        row.append(InlineKeyboardButton(ids[i], callback_data=f"copy_{ids[i]}"))
    if row:
        buttons.append(row)
    
    if end - start > 5:
        row = []
        for i in range(start + 5, end):
            row.append(InlineKeyboardButton(ids[i], callback_data=f"copy_{ids[i]}"))
        if row:
            buttons.append(row)
    
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton(f"📊 {page}/{pages}", callback_data="current"))
    if page < pages:
        nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"page_{page+1}"))
    buttons.append(nav)
    
    buttons.append([
        InlineKeyboardButton("📥 Extract", callback_data="go_extract"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh")
    ])
    
    await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

async def batches_callback(client, cb):
    data = cb.data
    uid = cb.from_user.id
    
    await cb.answer()
    
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await show_page(client, cb.message, uid, page)
    
    elif data.startswith("copy_"):
        bid = data.split("_")[1]
        await cb.answer(f"✅ Copied: {bid}", show_alert=True)
    
    elif data == "go_extract":
        await cb.message.delete()
        from .extract_handler import extract_command
        await extract_command(client, cb.message)
    
    elif data == "refresh":
        await cb.message.edit(f"{EMOJI['info']} Refreshing...")
        await all_batches_command(client, cb.message)
    
    elif data in ["help", "about", "extract", "batches"]:
        await cb.message.delete()
        if data == "help":
            from .help_handler import help_command
            await help_command(client, cb.message)
        elif data == "about":
            from .about_handler import about_command
            await about_command(client, cb.message)
        elif data == "extract":
            from .extract_handler import extract_command
            await extract_command(client, cb.message)
        elif data == "batches":
            await all_batches_command(client, cb.message)
