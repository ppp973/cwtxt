from pyrogram.types import Message
from config import EMOJI

async def help_command(client, message: Message):
    text = f"""
{EMOJI['info']} **CareerWill Bot Help Guide** {EMOJI['info']}

━━━━━━━━━━━━━━━━━━━━━━
**📥 /cwextractfree**
Extract any batch:
1. Send `/cwextractfree`
2. Enter Batch ID (e.g., `1377`)
3. Get .txt file with all links

**📚 /allbatches**
View all batches with clickable IDs

**🎯 Tips:**
- Multiple IDs: `1377 1840 2034`
- DRM videos marked with {EMOJI['drm']}
- 20 parallel workers for speed

━━━━━━━━━━━━━━━━━━━━━━
**⚡ @sdfvghhghhbnm_bot**
"""
    await message.reply_text(text)
