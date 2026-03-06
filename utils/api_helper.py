"""
CareerWill Bot - File Helper Module
Handles all file operations for the CareerWill Telegram Bot.
"""

import os
import re
import shutil
import aiofiles
import asyncio
import logging
import time
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Configuration
DOWNLOAD_DIR = "downloads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_FILENAME_LENGTH = 100
CLEANUP_AGE = 3600  # 1 hour in seconds

# ==================== DIRECTORY MANAGEMENT ====================

def ensure_download_dir():
    """Ensure download directory exists"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    logger.info(f"📁 Download directory: {os.path.abspath(DOWNLOAD_DIR)}")

def get_download_dir() -> str:
    """Get download directory path"""
    return os.path.abspath(DOWNLOAD_DIR)

# ==================== FILENAME OPERATIONS ====================

def sanitize_filename(filename: str, max_length: int = MAX_FILENAME_LENGTH) -> str:
    """
    Remove invalid characters from filename
    
    Args:
        filename: Original filename
        max_length: Maximum length
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    
    # Replace multiple spaces with single
    filename = re.sub(r'\s+', ' ', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > max_length:
        name_part = filename[:max_length-20]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name_part}_{timestamp}"
    
    return filename

def generate_filename(batch_name: str, batch_id: str, extension: str = '.txt') -> str:
    """
    Generate a unique filename for batch
    
    Args:
        batch_name: Name of the batch
        batch_id: Batch ID
        extension: File extension
    
    Returns:
        Generated filename
    """
    safe_name = sanitize_filename(batch_name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{safe_name}_{batch_id}_{timestamp}{extension}"

# ==================== FILE OPERATIONS ====================

async def save_to_file(batch_name: str, batch_id: str, items: List[str]) -> Optional[str]:
    """
    Save extracted items to a text file
    
    Args:
        batch_name: Name of the batch
        batch_id: Batch ID
        items: List of items to save
    
    Returns:
        Path to saved file or None
    """
    try:
        ensure_download_dir()
        
        # Generate filename
        filename = generate_filename(batch_name, batch_id)
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        
        # Write to file
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            for item in items:
                await f.write(item + '\n')
        
        logger.info(f"✅ File saved: {filename} ({len(items)} items)")
        return filepath
        
    except Exception as e:
        logger.error(f"File save error: {str(e)}")
        return None

async def read_from_file(filepath: str) -> Optional[List[str]]:
    """
    Read lines from a text file
    
    Args:
        filepath: Path to file
    
    Returns:
        List of lines or None
    """
    try:
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            return None
        
        async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
            content = await f.read()
            lines = content.split('\n')
            lines = [line for line in lines if line.strip()]
        
        logger.info(f"📖 Read {len(lines)} lines from {os.path.basename(filepath)}")
        return lines
        
    except Exception as e:
        logger.error(f"File read error: {str(e)}")
        return None

async def cleanup_file(filepath: str) -> bool:
    """
    Delete a file
    
    Args:
        filepath: Path to file
    
    Returns:
        True if deleted successfully
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"🗑️ Deleted: {os.path.basename(filepath)}")
            return True
        return False
    except Exception as e:
        logger.error(f"File delete error: {str(e)}")
        return False

# ==================== FILE VALIDATION ====================

def get_file_size(filepath: str) -> int:
    """Get file size in bytes"""
    try:
        if os.path.exists(filepath):
            return os.path.getsize(filepath)
        return 0
    except Exception as e:
        logger.error(f"File size error: {str(e)}")
        return 0

def is_valid_txt(filepath: str) -> bool:
    """Check if file is valid text file"""
    try:
        if not os.path.exists(filepath):
            return False
        
        if not filepath.endswith('.txt'):
            return False
        
        size = get_file_size(filepath)
        if size > MAX_FILE_SIZE:
            logger.warning(f"File too large: {size} bytes")
            return False
        
        return True
    except Exception as e:
        logger.error(f"File validation error: {str(e)}")
        return False

# ==================== CLEANUP ====================

def cleanup_old_files(age_seconds: int = CLEANUP_AGE) -> int:
    """Delete old files from download directory"""
    try:
        now = time.time()
        deleted = 0
        
        if not os.path.exists(DOWNLOAD_DIR):
            return 0
        
        for filename in os.listdir(DOWNLOAD_DIR):
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            
            if os.path.isfile(filepath):
                file_age = now - os.path.getmtime(filepath)
                
                if file_age > age_seconds:
                    os.remove(filepath)
                    deleted += 1
                    logger.debug(f"🗑️ Deleted old file: {filename}")
        
        if deleted > 0:
            logger.info(f"🧹 Cleaned up {deleted} old files")
        
        return deleted
        
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return 0

# ==================== INITIALIZATION ====================

# Create download directory on import
ensure_download_dir()

# Clean up old files on import
cleanup_old_files()

# Export all functions
__all__ = [
    'sanitize_filename',
    'save_to_file',
    'read_from_file',
    'cleanup_file',
    'ensure_download_dir',
    'get_download_dir',
    'generate_filename',
    'get_file_size',
    'is_valid_txt',
    'cleanup_old_files'
]
