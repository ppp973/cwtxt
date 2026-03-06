#!/usr/bin/env python3
"""
Handlers Package Initialization
CareerWill Premium Telegram Bot
"""

import logging

logger = logging.getLogger(__name__)

# ==================== COMMAND HANDLERS ====================

# सिर्फ ये इम्पोर्ट सही हैं - api_helper यहाँ नहीं आता
from .start_handler import start_command
from .help_handler import help_command
from .about_handler import about_command
from .extract_handler import extract_command
from .batches_handler import all_batches_command, batches_callback

# ==================== PACKAGE EXPORTS ====================

__all__ = [
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

# ==================== INITIALIZATION ====================

logger.info("✅ Handlers package loaded successfully")
