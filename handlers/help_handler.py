"""
Help command handler for CareerWill Bot
"""

from pyrogram.types import Message
from config import PREMIUM_COLORS as pc

async def help_command(client, message: Message):
    """Handle /help command with premium UI"""
    
    help_text = (
        f"{pc['info']} **CareerWill Extractor - Complete Guide** {pc['info']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**📥 /cwextractfree - Extract Batch**\n\n"
        f"**Step-by-Step:**\n"
        f"1️⃣ Send command: `/cwextractfree`\n"
        f"2️⃣ Enter Batch ID (e.g., `1377`)\n"
        f"3️⃣ Watch live extraction progress\n"
        f"4️⃣ Receive complete .txt file\n\n"
        f"**Example:**\n"
        f"```\n"
        f"/cwextractfree\n"
        f"Enter Batch ID: 1377\n"
        f"✓ Processing: 10th Class (VOD)...\n"
        f"✓ Found 45 videos, 12 PDFs\n"
        f"✓ File: 10th_Class_1377.txt\n"
        f"```\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**📚 /allbatches - View All Batches**\n\n"
        f"**Features:**\n"
        f"├ 📋 Complete batch list with IDs\n"
        f"├ 🔍 Click to copy any batch ID\n"
        f"├ 🎯 Premium paginated view\n"
        f"└ ⚡ Real-time search\n\n"
        f"**Example:**\n"
        f"```\n"
        f"/allbatches\n"
        f"📚 Page 1/10\n"
        f"├ 1377 - 10th Class (VOD)\n"
        f"├ 1840 - KVS 2023 Interview\n"
        f"└ 2034 - UPSC Foundation\n"
        f"```\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**🎯 Pro Tips:**\n\n"
        f"{pc['success']} **Multiple Batches:**\n"
        f"Extract multiple batches at once\n"
        f"`1377 1840 2034` (space-separated)\n\n"
        f"{pc['warning']} **DRM Detection:**\n"
        f"DRM videos are marked with {pc['drm']}\n\n"
        f"{pc['time']} **Speed Optimization:**\n"
        f"20 parallel workers for ultra-fast extraction\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**⚡ Need Help? Contact @sdfvghhghhbnm_bot**"
    )
    
    await message.reply_text(help_text)
