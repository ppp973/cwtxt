"""
CareerWill Bot - Utils Package
This package contains all utility functions for the CareerWill Telegram Bot.
"""

# Import all API helper functions
from .api_helper import (
    # Core functions
    fetch_json,
    fetch_with_retry,
    
    # Video functions
    get_video_url,
    get_video_details,
    
    # Batch functions
    get_batch_info,
    get_batch_details,
    get_topic_details,
    get_all_batches,
    
    # Extraction functions
    process_topic,
    extract_batch,
    extract_multiple_batches,
    
    # Progress tracking
    ExtractionProgress,
    format_progress_bar,
    
    # Statistics
    ExtractionStats,
    
    # Utility functions
    validate_batch_id,
    check_api_status
)

# Import all file helper functions
from .file_helper import (
    # File operations
    sanitize_filename,
    save_to_file,
    read_from_file,
    cleanup_file,
    cleanup_all_files,
    
    # File validation
    validate_file,
    get_file_size,
    is_valid_txt,
    
    # File formatting
    format_file_caption,
    generate_filename,
    
    # Directory management
    ensure_download_dir,
    get_download_dir,
    clear_download_dir,
    get_disk_usage,
    
    # Batch file operations
    merge_batch_files,
    split_large_file,
    
    # Encoding helpers
    detect_encoding,
    convert_encoding
)

# Version info
__version__ = "3.0.0"
__author__ = "Ayushxsdy"
__description__ = "CareerWill Premium Bot Utils Package"

# Package metadata
__all__ = [
    # API Helper exports
    'fetch_json',
    'fetch_with_retry',
    'get_video_url',
    'get_video_details',
    'get_batch_info',
    'get_batch_details',
    'get_topic_details',
    'get_all_batches',
    'process_topic',
    'extract_batch',
    'extract_multiple_batches',
    'ExtractionProgress',
    'format_progress_bar',
    'ExtractionStats',
    'validate_batch_id',
    'check_api_status',
    
    # File Helper exports
    'sanitize_filename',
    'save_to_file',
    'read_from_file',
    'cleanup_file',
    'cleanup_all_files',
    'validate_file',
    'get_file_size',
    'is_valid_txt',
    'format_file_caption',
    'generate_filename',
    'ensure_download_dir',
    'get_download_dir',
    'clear_download_dir',
    'get_disk_usage',
    'merge_batch_files',
    'split_large_file',
    'detect_encoding',
    'convert_encoding'
]

# Package initialization
def initialize_utils():
    """Initialize all utility modules"""
    from .api_helper import initialize_api
    from .file_helper import initialize_file_system
    
    # Initialize API
    initialize_api()
    
    # Initialize file system
    initialize_file_system()
    
    return True

# Run initialization
initialize_utils()

# Package information
def get_package_info():
    """Get package information"""
    return {
        'name': 'careerwill_utils',
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'modules': ['api_helper', 'file_helper'],
        'features': [
            'Batch Extraction',
            'Video Processing',
            'PDF Extraction',
            'File Management',
            'Progress Tracking',
            'Statistics Generation'
        ]
    }

# Error classes
class UtilsError(Exception):
    """Base exception for utils package"""
    pass

class APIError(UtilsError):
    """API related errors"""
    pass

class FileError(UtilsError):
    """File operation errors"""
    pass

class ValidationError(UtilsError):
    """Validation errors"""
    pass

# Logging setup
import logging
logger = logging.getLogger(__name__)

def setup_logging(level=logging.INFO):
    """Setup logging for utils package"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.setLevel(level)
    logger.info("✅ Utils package logging initialized")

# Call setup
setup_logging()

# Export all
__all__.extend([
    'UtilsError',
    'APIError',
    'FileError',
    'ValidationError',
    'get_package_info'
])
