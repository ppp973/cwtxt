import os

# Telegram API Credentials
API_ID = 21503125
API_HASH = "bab9855c442e9e4e87f413cb5b9dc3f9"
BOT_TOKEN = "8768725493:AAFDhnWucAWD9Tl9djbRtOr6v5bUUOFmCQY"

# Channel ID for logs
CHANNEL_ID = -1003724248856

# Batch API
BATCH_API = "https://cw-api-website.vercel.app/batch/{}"
TOPIC_API = "https://cw-api-website.vercel.app/batch?batchid={}&topicid={}&full=true"
VIDEO_API = "https://cw-vid-virid.vercel.app/get_video_details?name={}"
ALL_BATCHES_API = "https://cw-api-website.vercel.app/batches"

# Bot Settings
MAX_WORKERS = 20
DOWNLOAD_DIR = "downloads"
TIMEOUT = 30

# Premium UI Settings
PREMIUM_COLORS = {
    "primary": "🔵",
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
    "info": "ℹ️",
    "video": "🎥",
    "pdf": "📄",
    "drm": "🔒",
    "time": "⏱️",
    "stats": "📊",
    "batch": "📚",
    "topic": "📑",
    "class": "📺"
}

print("✅ Configuration loaded successfully!")
