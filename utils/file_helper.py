import os
import re
import aiofiles
import logging
from datetime import datetime
from config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)

def sanitize_filename(filename, max_length=100):
    """Remove invalid characters from filename"""
    # Remove invalid characters
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Limit length
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename

async def save_to_file(batch_name, batch_id, items):
    """Save extracted items to a text file"""
    try:
        # Create downloads directory if not exists
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        
        # Generate filename
        safe_name = sanitize_filename(batch_name)
        filename = f"{DOWNLOAD_DIR}/{safe_name}_{batch_id}.txt"
        
        # Write to file
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            for item in items:
                await f.write(item + '\n')
        
        logger.info(f"✅ File saved: {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"File save error: {str(e)}")
        return None

async def cleanup_file(filepath):
    """Delete file after sending"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"🗑️ Cleaned up: {filepath}")
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
