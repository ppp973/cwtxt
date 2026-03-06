from pyrogram import filters
from pyrogram.types import Message
from config import PREMIUM_COLORS as pc

async def about_command(client, message: Message):
    """Handle /about command"""
    
    about_text = f"""
{pc['primary']} **🤖 About CareerWill Premium Bot** {pc['primary']}

━━━━━━━━━━━━━━━━━━━━━━
**📊 Bot Statistics:**

├ **Version:** `3.0.0`
├ **Language:** Python 3.10
├ **Framework:** Pyrogram 2.0
├ **Developer:** @Ayushxsdy
└ **Released:** March 2026

━━━━━━━━━━━━━━━━━━━━━━
**✨ Premium Features:**

{pc['success']} **Ultra-Fast Extraction**
├ 20 parallel workers
├ 3x retry mechanism
└ 30-second timeout

{pc['stats']} **Live Progress**
├ Real-time topic tracking
├ File count estimation
└ Time remaining display

{pc['video']} **Smart Detection**
├ Auto DRM detection
├ PDF validation
└ Duplicate removal

{pc['batch']} **Batch Management**
├ Single batch extraction
├ Multiple batch support
└ Batch ID copier

━━━━━━━━━━━━━━━━━━━━━━
**🔧 Technical Specifications:**

├ **Max Workers:** 20
├ **Timeout:** 30 seconds
├ **Retries:** 3 attempts
├ **File Limit:** 50MB
└ **Concurrent Users:** Unlimited

━━━━━━━━━━━━━━━━━━━━━━
**⚡ Made with ❤️ for CareerWill Students**
"""
    
    await message.reply_text(about_text)
