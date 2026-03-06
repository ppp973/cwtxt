from pyrogram.types import Message
from config import EMOJI

async def about_command(client, message: Message):
    text = f"""
{EMOJI['primary']} **About CareerWill Bot** {EMOJI['primary']}

━━━━━━━━━━━━━━━━━━━━━━
**Version:** 3.0.0
**Language:** Python 3.10
**Framework:** Pyrogram
**Developer:** @Ayushxsdy

**Features:**
✓ 20 parallel workers
✓ Live progress tracking
✓ DRM detection
✓ Multiple batch support

━━━━━━━━━━━━━━━━━━━━━━
**⚡ Made with ❤️**
"""
    await message.reply_text(text)
