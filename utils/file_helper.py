import os
import re
import aiofiles
import logging
from datetime import datetime
from config import DOWNLOAD_DIR, MAX_FILENAME_LENGTH

logger = logging.getLogger(__name__)

def ensure_download_dir():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    filename = filename.replace(' ', '_')
    filename = re.sub(r'_+', '_', filename)
    return filename.strip('_')[:MAX_FILENAME_LENGTH]

def generate_filename(batch_name: str, batch_id: str) -> str:
    safe_name = sanitize_filename(batch_name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{safe_name}_{batch_id}_{timestamp}.txt"

async def save_to_file(batch_name: str, batch_id: str, items: list) -> str:
    ensure_download_dir()
    filename = generate_filename(batch_name, batch_id)
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        for item in items:
            await f.write(item + '\n')
    
    logger.info(f"✅ Saved: {filename} ({len(items)} items)")
    return filepath

async def read_from_file(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
        content = await f.read()
        return [line for line in content.split('\n') if line.strip()]

async def cleanup_file(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"🗑️ Deleted: {os.path.basename(filepath)}")
    except:
        pass

ensure_download_dir()
