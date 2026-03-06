"""
Utils package for CareerWill Bot
Contains all utility functions for API calls and file operations.
"""

from .api_helper import (
    # Core functions
    fetch_json,
    get_video_url,
    get_batch_info,
    get_topic_details,
    get_all_batches,
    process_topic,
    extract_batch,
    ExtractionProgress,  # अब यह मौजूद है
    ExtractionStats,      # अब यह मौजूद है
    validate_batch_id,
    check_api_status
)

from .file_helper import (
    sanitize_filename,
    save_to_file,
    read_from_file,
    cleanup_file,
    ensure_download_dir,
    generate_filename
)

__all__ = [
    # API Helper exports
    'fetch_json',
    'get_video_url',
    'get_batch_info',
    'get_topic_details',
    'get_all_batches',
    'process_topic',
    'extract_batch',
    'ExtractionProgress',
    'ExtractionStats',
    'validate_batch_id',
    'check_api_status',
    
    # File Helper exports
    'sanitize_filename',
    'save_to_file',
    'read_from_file',
    'cleanup_file',
    'ensure_download_dir',
    'generate_filename'
]

__version__ = '3.0.0'
__author__ = 'Ayushxsdy'

import logging
logger = logging.getLogger(__name__)
logger.info("✅ Utils package initialized with all required classes")
