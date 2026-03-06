from pyrogram import filters
from pyrogram.types import Message
from config import PREMIUM_COLORS as pc

async def help_command(client, message: Message):
    """Handle /help command"""
    
    help_text = f"""
{pc['info']} **CareerWill Extractor - Complete Guide** {pc['info']}

━━━━━━━━━━━━━━━━━━━━━━
**📥 /cwextractfree - Extract Batch**

**Step-by-Step:**
1️⃣ Send command: `/cwextractfree`
2️⃣ Enter Batch ID (e.g., `1377`)
3️⃣ Watch live extraction progress
4️⃣ Receive complete .txt file

**Example:**
