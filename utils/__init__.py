"""
Utils package for CareerWill Bot
"""

from .api_helper import (
    fetch_json,
    get_video_url,
    get_batch_info,
    get_topic_details,
    get_all_batches,
    process_topic,
    extract_batch,
    validate_batch_id,
    ExtractionProgress,
    ExtractionStats
)

from .file_helper import (
    sanitize_filename,
    generate_filename,
    save_to_file,
    read_from_file,
    cleanup_file,
    ensure_download_dir
)

__all__ = [
    'fetch_json', 'get_video_url', 'get_batch_info', 'get_topic_details',
    'get_all_batches', 'process_topic', 'extract_batch', 'validate_batch_id',
    'ExtractionProgress', 'ExtractionStats',
    'sanitize_filename', 'generate_filename', 'save_to_file',
    'read_from_file', 'cleanup_file', 'ensure_download_dir'
]

import logging
logger = logging.getLogger(__name__)
logger.info("✅ Utils package initialized")
