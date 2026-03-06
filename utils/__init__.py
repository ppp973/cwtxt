#!/usr/bin/env python3
"""
Handlers Package Initialization
CareerWill Premium Telegram Bot

This package contains all command handlers for the bot:
- /start - Welcome message
- /help - Help guide
- /about - Bot information
- /cwextractfree - Extract batch
- /allbatches - View all batches
"""

import logging
from typing import Dict, Any

# Configure logger for handlers package
logger = logging.getLogger(__name__)

# ==================== COMMAND HANDLERS ====================

# Import all handler functions
from .start_handler import start_command
from .help_handler import help_command
from .about_handler import about_command
from .extract_handler import extract_command
from .batches_handler import all_batches_command, batches_callback

# ==================== PACKAGE EXPORTS ====================

# Define what gets imported with "from handlers import *"
__all__ = [
    # Command handlers
    'start_command',
    'help_command', 
    'about_command',
    'extract_command',
    'all_batches_command',
    'batches_callback',
    
    # Package metadata (will be added below)
]

# ==================== PACKAGE METADATA ====================

__version__ = '3.0.0'
__author__ = 'Ayushxsdy'
__description__ = 'CareerWill Premium Bot - Command Handlers Package'
__license__ = 'MIT'

# ==================== PACKAGE INITIALIZATION ====================

def initialize_handlers() -> bool:
    """
    Initialize all handlers package
    
    Returns:
        bool: True if initialization successful
    """
    try:
        logger.info("🚀 Initializing handlers package...")
        
        # Log all available handlers
        handlers_list = [
            'start_command',
            'help_command',
            'about_command', 
            'extract_command',
            'all_batches_command',
            'batches_callback'
        ]
        
        logger.info(f"📋 Registered handlers: {', '.join(handlers_list)}")
        logger.info("✅ Handlers package initialized successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize handlers: {str(e)}")
        return False

# ==================== PACKAGE INFORMATION ====================

def get_package_info() -> Dict[str, Any]:
    """
    Get handlers package information
    
    Returns:
        Dict with package metadata
    """
    return {
        'name': 'handlers',
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'license': __license__,
        'handlers': [
            'start_command',
            'help_command',
            'about_command',
            'extract_command',
            'all_batches_command',
            'batches_callback'
        ],
        'features': [
            'Welcome message with premium UI',
            'Detailed help guide',
            'Bot information',
            'Batch extraction with progress tracking',
            'All batches view with pagination',
            'Click-to-copy batch IDs',
            'Multiple batch support',
            'Real-time progress updates'
        ]
    }

# ==================== ERROR HANDLING ====================

class HandlersError(Exception):
    """Base exception for handlers package"""
    pass

class CommandNotFoundError(HandlersError):
    """Raised when command is not found"""
    pass

class HandlerExecutionError(HandlersError):
    """Raised when handler execution fails"""
    pass

# ==================== RUN INITIALIZATION ====================

# Auto-initialize when package is imported
if not initialize_handlers():
    logger.warning("⚠️ Handlers package initialization had issues")

# ==================== EXPORT EVERYTHING ====================

# Add error classes to exports
__all__.extend([
    'HandlersError',
    'CommandNotFoundError',
    'HandlerExecutionError',
    'get_package_info',
    'initialize_handlers'
])

# ==================== CLEANUP ====================

def cleanup_handlers():
    """Cleanup handlers package resources"""
    logger.info("🧹 Cleaning up handlers package...")
    # Add any cleanup code here if needed

import atexit
atexit.register(cleanup_handlers)

# ==================== END OF FILE ====================
