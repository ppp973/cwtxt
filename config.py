#!/usr/bin/env python3
"""
Configuration file for CareerWill Premium Bot
COMPLETE WORKING VERSION
"""

# ==================== TELEGRAM API CREDENTIALS ====================
API_ID = 21503125
API_HASH = "bab9855c442e9e4e87f413cb5b9dc3f9"
BOT_TOKEN = "8768725493:AAFDhnWucAWD9Tl9djbRtOr6v5bUUOFmCQY"

# Channel ID for logs - OPTIONAL (set to None if not using)
CHANNEL_ID = None  # या अपना चैनल आईडी डालें: -1003724248856

# ==================== API ENDPOINTS ====================
BATCH_API = "https://cw-api-website.vercel.app/batch/{}"
TOPIC_API = "https://cw-api-website.vercel.app/batch?batchid={}&topicid={}&full=true"
VIDEO_API = "https://cw-vid-virid.vercel.app/get_video_details?name={}"
ALL_BATCHES_API = "https://cw-api-website.vercel.app/batches"

# ==================== PERFORMANCE SETTINGS ====================
MAX_WORKERS = 20
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2

# ==================== FILE SETTINGS ====================
DOWNLOAD_DIR = "downloads"
MAX_FILENAME_LENGTH = 100

# ==================== PREMIUM UI EMOJIS ====================
EMOJI = {
    "primary": "🔵", "success": "✅", "warning": "⚠️", "error": "❌",
    "info": "ℹ️", "video": "🎥", "pdf": "📄", "drm": "🔒", "time": "⏱️",
    "stats": "📊", "batch": "📚", "topic": "📑", "class": "📺",
    "download": "📥", "upload": "📤", "processing": "🔄", "completed": "✨"
}

print("✅ Configuration loaded successfully!")
