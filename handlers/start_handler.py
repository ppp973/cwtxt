
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import EMOJI

async def start_command(client, message: Message):
    text = f"""
{EMOJI['primary']} **Welcome to CareerWill Premium Bot** {EMOJI['primary']}

━━━━━━━━━━━━━━━━━━━━━━
**📋 Available Commands:**

{EMOJI['primary']} **/start** - Show this message
{EMOJI['info']} **/help** - Help guide
{EMOJI['batch']} **/about** - Bot info
{EMOJI['video']} **/cwextractfree** - Extract batch
{EMOJI['batch']} **/allbatches** - View all batches

━━━━━━━━━━━━━━━━━━━━━━
**⚡ @sdfvghhghhbnm_bot**
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Extract", callback_data="extract"),
         InlineKeyboardButton("📚 Batches", callback_data="batches")],
        [InlineKeyboardButton("❓ Help", callback_data="help"),
         InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])
    
    await message.reply_text(text, reply_markup=keyboard)
