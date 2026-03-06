from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import PREMIUM_COLORS as pc

async def start_command(client, message: Message):
    """Handle /start command"""
    
    # Premium UI Welcome Message
    welcome_text = f"""
{pc['primary']} **Welcome to CareerWill Premium Extractor Bot** {pc['primary']}

━━━━━━━━━━━━━━━━━━━━━━
**🤖 Bot Features:**

{pc['batch']} **Batch Extraction**
├ Extract any CareerWill batch
├ Videos + PDFs support
└ DRM content detection

{pc['stats']} **Real-time Stats**
├ Live progress tracking
├ Time estimation
└ Detailed summary

{pc['success']} **Premium Features**
├ 20x parallel processing
├ Zero downtime
└ 99.9% success rate

━━━━━━━━━━━━━━━━━━━━━━
**📋 Available Commands:**

{pc['primary']} **/start** - Show this message
{pc['info']} **/help** - Detailed guide
{pc['about']} **/about** - Bot information
{pc['video']} **/cwextractfree** - Extract batch
{pc['batch']} **/allbatches** - View all batches

━━━━━━━━━━━━━━━━━━━━━━
**⚡ Powered by @sdfvghhghhbnm_bot**
"""
    
    # Premium Inline Keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📥 Extract Batch", callback_data="extract"),
            InlineKeyboardButton("📚 All Batches", callback_data="batches")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ]
    ])
    
    await message.reply_text(
        welcome_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
