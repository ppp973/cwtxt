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

# Configure logger for handlers package
logger = logging.getLogger(__name__)

# ==================== COMMAND HANDLERS ====================

# Import all handler functions from their respective modules
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
]

# ==================== PACKAGE METADATA ====================

__version__ = '3.0.0'
__author__ = 'Ayushxsdy'
__description__ = 'CareerWill Premium Bot - Command Handlers Package'

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

# Auto-initialize when package is imported
initialize_handlers()

# ==================== END OF FILE ====================
