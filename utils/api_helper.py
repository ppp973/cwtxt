"""
CareerWill Bot - API Helper Module
Handles all API calls to CareerWill servers with retry mechanism and error handling.
"""

import requests
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)

# API Endpoints
BATCH_API = "https://cw-api-website.vercel.app/batch/{}"
TOPIC_API = "https://cw-api-website.vercel.app/batch?batchid={}&topicid={}&full=true"
VIDEO_API = "https://cw-vid-virid.vercel.app/get_video_details?name={}"
ALL_BATCHES_API = "https://cw-api-website.vercel.app/batches"

# Configuration
MAX_WORKERS = 20
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2

# Session for connection reuse
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
})

# ==================== CORE API FUNCTIONS ====================

def fetch_json(url: str, retries: int = MAX_RETRIES) -> Optional[Dict]:
    """
    Fetch JSON from URL with retry mechanism
    
    Args:
        url: URL to fetch
        retries: Number of retry attempts
    
    Returns:
        JSON data or None if failed
    """
    for attempt in range(retries):
        try:
            logger.debug(f"📡 Fetching [{attempt+1}/{retries}]: {url[:100]}...")
            
            response = session.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.debug(f"✅ Success: {len(str(data))} bytes")
                    return data
                except json.JSONDecodeError:
                    logger.error(f"❌ Invalid JSON response")
                    return None
            else:
                logger.warning(f"⚠️ HTTP {response.status_code}")
                
                # Rate limiting detection
                if response.status_code == 429:
                    wait_time = RETRY_DELAY * (attempt + 1) * 2
                    logger.info(f"⏳ Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    
        except requests.exceptions.Timeout:
            logger.warning(f"⏰ Timeout attempt {attempt+1}/{retries}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"🔌 Connection error attempt {attempt+1}/{retries}")
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
        
        if attempt < retries - 1:
            time.sleep(RETRY_DELAY * (attempt + 1))
    
    logger.error(f"❌ Failed after {retries} attempts")
    return None

# ==================== VIDEO FUNCTIONS ====================

def get_video_url(video_id: str) -> Optional[str]:
    """
    Get actual video URL from video ID
    
    Args:
        video_id: Video ID or name
    
    Returns:
        Video URL or None
    """
    try:
        data = fetch_json(VIDEO_API.format(video_id))
        
        if not data:
            return None
        
        # Try different response structures
        if isinstance(data, dict):
            # Structure 1: {"data": {"link": {"file_url": "..."}}}
            if "data" in data:
                if "link" in data["data"]:
                    return data["data"]["link"].get("file_url")
                return data["data"].get("file_url")
            
            # Structure 2: {"file_url": "..."}
            if "file_url" in data:
                return data["file_url"]
            
            # Structure 3: {"url": "..."}
            if "url" in data:
                return data["url"]
            
            # Structure 4: {"link": "..."}
            if "link" in data:
                if isinstance(data["link"], dict):
                    return data["link"].get("file_url")
                return data["link"]
        
        return None
        
    except Exception as e:
        logger.error(f"Video URL fetch error: {str(e)}")
        return None

# ==================== BATCH FUNCTIONS ====================

def get_batch_info(batch_id: str) -> Optional[Dict]:
    """
    Get basic batch information
    
    Args:
        batch_id: Batch ID
    
    Returns:
        Batch information or None
    """
    return fetch_json(BATCH_API.format(batch_id))

def get_topic_details(batch_id: str, topic_id: str) -> Optional[Dict]:
    """
    Get detailed topic information including videos and PDFs
    
    Args:
        batch_id: Batch ID
        topic_id: Topic ID
    
    Returns:
        Topic details or None
    """
    return fetch_json(TOPIC_API.format(batch_id, topic_id))

def get_all_batches() -> Optional[Dict[str, str]]:
    """
    Get all available batches with their names
    
    Returns:
        Dictionary with batch_id as key and batch_name as value
    """
    data = fetch_json(ALL_BATCHES_API)
    
    if data and isinstance(data, dict):
        return data
    
    return None

# ==================== EXTRACTION FUNCTIONS ====================

def process_topic(batch_id: str, topic: Dict) -> List[Dict]:
    """
    Process a single topic and extract all content
    
    Args:
        batch_id: Batch ID
        topic: Topic dictionary with id and name
    
    Returns:
        List of extracted items
    """
    try:
        topic_id = topic.get("id") or topic.get("topicId")
        topic_name = topic.get("topicName") or topic.get("name") or "Unknown Topic"
        
        if not topic_id:
            logger.warning(f"⚠️ Topic without ID: {topic_name}")
            return []
        
        # Get topic details
        topic_data = get_topic_details(batch_id, topic_id)
        
        if not topic_data:
            logger.warning(f"⚠️ No data for topic: {topic_name}")
            return []
        
        results = []
        
        # Extract videos from classes
        classes = topic_data.get("classes", [])
        for cls in classes:
            title = cls.get("title", "Untitled Class")
            class_no = cls.get("class_no", "")
            video_id = cls.get("video_url")
            
            if video_id:
                video_url = get_video_url(video_id)
                
                if video_url:
                    results.append({
                        "type": "drm" if video_url.endswith('.mpd') else "video",
                        "topic": topic_name,
                        "class_no": class_no,
                        "title": title,
                        "url": video_url,
                        "line": f"[{topic_name}] Class {class_no} | {title}: {video_url}"
                    })
        
        # Extract PDFs from notes
        notes = topic_data.get("notes", [])
        for note in notes:
            title = note.get("title", "Untitled PDF")
            pdf_url = note.get("view_url") or note.get("download_url")
            
            if pdf_url and pdf_url.endswith('.pdf'):
                results.append({
                    "type": "pdf",
                    "topic": topic_name,
                    "title": title,
                    "url": pdf_url,
                    "line": f"[{topic_name}] PDF | {title}: {pdf_url}"
                })
        
        return results
        
    except Exception as e:
        logger.error(f"Topic processing error: {str(e)}")
        return []

def extract_batch(batch_id: str, progress_callback: Optional[Callable] = None) -> Optional['ExtractionStats']:
    """
    Extract all content from a batch
    
    Args:
        batch_id: Batch ID to extract
        progress_callback: Optional progress callback
    
    Returns:
        ExtractionStats object or None if failed
    """
    start_time = time.time()
    logger.info(f"🚀 Starting extraction for batch: {batch_id}")
    
    # Get batch info
    batch = get_batch_info(batch_id)
    
    if not batch:
        logger.error(f"❌ Batch not found: {batch_id}")
        return None
    
    batch_name = batch.get("batch_name") or batch.get("name") or f"Batch_{batch_id}"
    topics = batch.get("topics", [])
    
    if not topics:
        logger.warning(f"⚠️ No topics in batch: {batch_name}")
        return ExtractionStats(
            batch_id=batch_id,
            batch_name=batch_name,
            total_items=0,
            videos=0,
            pdfs=0,
            drm_count=0,
            time_taken=time.time() - start_time,
            topics_processed=0,
            failed_topics=0,
            success_rate=0
        )
    
    # Initialize progress tracking
    progress = ExtractionProgress(len(topics))
    
    all_items = []
    failed_topics = 0
    drm_count = 0
    
    # Process topics in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        
        for topic in topics:
            future = executor.submit(process_topic, batch_id, topic)
            futures.append(future)
        
        completed = 0
        
        for future in as_completed(futures):
            completed += 1
            
            try:
                topic_items = future.result(timeout=TIMEOUT)
                
                if topic_items:
                    all_items.extend(topic_items)
                    
                    # Count by type
                    videos = sum(1 for i in topic_items if i['type'] == 'video')
                    pdfs = sum(1 for i in topic_items if i['type'] == 'pdf')
                    drm = sum(1 for i in topic_items if i['type'] == 'drm')
                    
                    drm_count += drm
                    
                    # Update progress
                    if topic_items:
                        current_topic = topic_items[0]['topic']
                        progress.update(current_topic, videos, pdfs)
                        
                        if progress_callback:
                            progress_callback(progress.get_status_line())
                else:
                    failed_topics += 1
                    
            except Exception as e:
                logger.error(f"Future error: {str(e)}")
                failed_topics += 1
    
    # Calculate statistics
    videos_count = sum(1 for i in all_items if i['type'] == 'video')
    pdfs_count = sum(1 for i in all_items if i['type'] == 'pdf')
    drm_count = sum(1 for i in all_items if i['type'] == 'drm')
    
    total_topics = len(topics)
    success_rate = ((total_topics - failed_topics) / total_topics) * 100 if total_topics > 0 else 0
    
    elapsed_time = time.time() - start_time
    
    logger.info(f"✅ Extraction completed in {elapsed_time:.2f}s")
    logger.info(f"📊 Found: {videos_count} videos, {pdfs_count} PDFs, {drm_count} DRM")
    
    # Create stats object
    stats = ExtractionStats(
        batch_id=batch_id,
        batch_name=batch_name,
        total_items=len(all_items),
        videos=videos_count,
        pdfs=pdfs_count,
        drm_count=drm_count,
        time_taken=elapsed_time,
        topics_processed=total_topics - failed_topics,
        failed_topics=failed_topics,
        success_rate=success_rate
    )
    
    # Store items in stats for later use
    stats.items = all_items
    
    return stats

# ==================== UTILITY FUNCTIONS ====================

def validate_batch_id(batch_id: str) -> bool:
    """
    Validate if batch ID exists
    
    Args:
        batch_id: Batch ID to validate
    
    Returns:
        True if batch exists
    """
    try:
        batch = get_batch_info(batch_id)
        return batch is not None
    except:
        return False

def check_api_status() -> Dict:
    """
    Check status of all APIs
    
    Returns:
        Dictionary with API status
    """
    status = {}
    
    # Check main API
    try:
        r = session.get(ALL_BATCHES_API, timeout=5)
        status['main_api'] = r.status_code == 200
    except:
        status['main_api'] = False
    
    return status

# ==================== PROGRESS CLASSES ====================

class ExtractionProgress:
    """Progress tracking for extraction"""
    def __init__(self, total_topics):
        self.total_topics = total_topics
        self.completed_topics = 0
        self.total_videos = 0
        self.total_pdfs = 0
        self.current_topic = ""
        self.start_time = time.time()
        self.estimated_time = 0
    
    def update(self, topic_name, videos=0, pdfs=0):
        """Update progress"""
        self.completed_topics += 1
        self.current_topic = topic_name
        self.total_videos += videos
        self.total_pdfs += pdfs
        
        elapsed = time.time() - self.start_time
        if self.completed_topics > 0:
            avg_time = elapsed / self.completed_topics
            remaining = self.total_topics - self.completed_topics
            self.estimated_time = avg_time * remaining
    
    def get_percentage(self) -> float:
        """Get completion percentage"""
        if self.total_topics == 0:
            return 0
        return (self.completed_topics / self.total_topics) * 100
    
    def get_status_line(self) -> str:
        """Get formatted status line"""
        percentage = self.get_percentage()
        bar = '█' * int(percentage/5) + '░' * (20 - int(percentage/5))
        
        status = f"📊 Progress: {bar} {percentage:.1f}%\n"
        status += f"├ Topics: {self.completed_topics}/{self.total_topics}\n"
        status += f"├ Videos: {self.total_videos}\n"
        status += f"├ PDFs: {self.total_pdfs}\n"
        
        if self.estimated_time > 0:
            mins = int(self.estimated_time // 60)
            secs = int(self.estimated_time % 60)
            status += f"└ ⏱️ ETA: {mins}m {secs}s"
        
        return status

class ExtractionStats:
    """Extraction statistics"""
    def __init__(self, batch_id, batch_name, total_items, videos, pdfs, 
                 drm_count, time_taken, topics_processed, failed_topics, success_rate):
        self.batch_id = batch_id
        self.batch_name = batch_name
        self.total_items = total_items
        self.videos = videos
        self.pdfs = pdfs
        self.drm_count = drm_count
        self.time_taken = time_taken
        self.topics_processed = topics_processed
        self.failed_topics = failed_topics
        self.success_rate = success_rate
        self.items = []

# Cleanup
def cleanup_api():
    """Cleanup API resources"""
    session.close()
    logger.info("🧹 API session closed")

import atexit
atexit.register(cleanup_api)

__all__ = [
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
    'check_api_status'
]
