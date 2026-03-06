"""
CareerWill Bot - File Helper Module
Handles all file operations.
"""

import os
import re
import aiofiles
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DOWNLOAD_DIR = "downloads"

def ensure_download_dir():
    """Ensure download directory exists"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    return filename.strip().replace(' ', '_')[:100]

def generate_filename(batch_name: str, batch_id: str) -> str:
    """Generate a unique filename"""
    safe_name = sanitize_filename(batch_name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{safe_name}_{batch_id}_{timestamp}.txt"

async def save_to_file(batch_name: str, batch_id: str, items: list) -> str:
    """Save items to a text file"""
    ensure_download_dir()
    filename = generate_filename(batch_name, batch_id)
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        for item in items:
            await f.write(item + '\n')
    
    logger.info(f"✅ Saved: {filename}")
    return filepath

async def read_from_file(filepath: str) -> list:
    """Read lines from a text file"""
    if not os.path.exists(filepath):
        return []
    
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
        content = await f.read()
        return [line for line in content.split('\n') if line.strip()]

async def cleanup_file(filepath: str):
    """Delete a file"""
    if os.path.exists(filepath):
        os.remove(filepath)
        logger.info(f"🗑️ Deleted: {os.path.basename(filepath)}")

__all__ = [
    'ensure_download_dir', 'sanitize_filename', 'generate_filename',
    'save_to_file', 'read_from_file', 'cleanup_file'
]
