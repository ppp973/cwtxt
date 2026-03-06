"""
Handlers package for CareerWill Bot
"""

from .start_handler import start_command
from .help_handler import help_command
from .about_handler import about_command
from .extract_handler import extract_command
from .batches_handler import all_batches_command, batches_callback

__all__ = [
    'start_command', 'help_command', 'about_command',
    'extract_command', 'all_batches_command', 'batches_callback'
]

import logging
logger = logging.getLogger(__name__)
logger.info("✅ Handlers package initialized")
