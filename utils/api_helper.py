import requests
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Callable, Any
from config import MAX_WORKERS, TIMEOUT, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)

# ==================== UPDATED API ENDPOINTS ====================
# Try different endpoints if one fails
BATCH_API_ENDPOINTS = [
    "https://cw-api-website.vercel.app/batch/{}",
    "https://api.careerwill.com/batch/{}",
    "https://cw-api.render.com/batch/{}"
]

TOPIC_API_ENDPOINTS = [
    "https://cw-api-website.vercel.app/batch?batchid={}&topicid={}&full=true",
    "https://api.careerwill.com/topic?batch={}&topic={}",
    "https://cw-api.render.com/details?batch={}&topic={}"
]

VIDEO_API_ENDPOINTS = [
    "https://cw-vid-virid.vercel.app/get_video_details?name={}",
    "https://api.careerwill.com/video/{}",
    "https://cw-vid.render.com/details?video={}"
]

ALL_BATCHES_ENDPOINTS = [
    "https://cw-api-website.vercel.app/batches",
    "https://api.careerwill.com/batches",
    "https://cw-api.render.com/all-batches"
]

# Session for connection reuse
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def fetch_json(urls: list, retries: int = MAX_RETRIES) -> Optional[Dict]:
    """Try multiple URLs for same resource"""
    for url in urls:
        for attempt in range(retries):
            try:
                logger.debug(f"Trying: {url[:100]}...")
                response = session.get(url, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"HTTP {response.status_code} for {url[:50]}")
                    
                if response.status_code == 429:  # Rate limit
                    time.sleep(RETRY_DELAY * (attempt + 1) * 2)
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout for {url[:50]}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {url[:50]}")
            except Exception as e:
                logger.error(f"Error: {e}")
            
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    
    return None

def get_video_url(video_id: str) -> Optional[str]:
    """Get actual video URL from video ID"""
    try:
        data = fetch_json([api.format(video_id) for api in VIDEO_API_ENDPOINTS])
        if not data:
            return None
        
        # Try different response structures
        if isinstance(data, dict):
            if "file_url" in data:
                return data["file_url"]
            if "data" in data and isinstance(data["data"], dict):
                if "link" in data["data"]:
                    return data["data"]["link"].get("file_url")
                return data["data"].get("file_url")
            if "url" in data:
                return data["url"]
            if "link" in data:
                return data["link"] if isinstance(data["link"], str) else data["link"].get("file_url")
        
        return None
    except Exception as e:
        logger.error(f"Video error: {e}")
        return None

def get_batch_info(batch_id: str) -> Optional[Dict]:
    """Get batch information"""
    return fetch_json([api.format(batch_id) for api in BATCH_API_ENDPOINTS])

def get_topic_details(batch_id: str, topic_id: str) -> Optional[Dict]:
    """Get topic details"""
    return fetch_json([api.format(batch_id, topic_id) for api in TOPIC_API_ENDPOINTS])

def get_all_batches() -> Optional[Dict[str, str]]:
    """Get all available batches"""
    return fetch_json(ALL_BATCHES_ENDPOINTS)

def process_topic(batch_id: str, topic: Dict) -> List[Dict]:
    """Process a single topic and extract content"""
    results = []
    try:
        topic_id = topic.get("id") or topic.get("topicId")
        topic_name = topic.get("topicName") or topic.get("name") or "Unknown"
        
        if not topic_id:
            return results
        
        topic_data = get_topic_details(batch_id, topic_id)
        if not topic_data:
            return results
        
        # Extract videos
        for cls in topic_data.get("classes", []):
            video_id = cls.get("video_url")
            if video_id:
                video_url = get_video_url(video_id)
                if video_url:
                    results.append({
                        "type": "drm" if video_url.endswith('.mpd') else "video",
                        "topic": topic_name,
                        "title": cls.get("title", ""),
                        "class_no": cls.get("class_no", ""),
                        "url": video_url,
                        "line": f"[{topic_name}] {cls.get('title', '')}: {video_url}"
                    })
        
        # Extract PDFs
        for note in topic_data.get("notes", []):
            pdf_url = note.get("view_url") or note.get("download_url")
            if pdf_url and pdf_url.endswith('.pdf'):
                results.append({
                    "type": "pdf",
                    "topic": topic_name,
                    "title": note.get("title", ""),
                    "url": pdf_url,
                    "line": f"[{topic_name}] PDF - {note.get('title', '')}: {pdf_url}"
                })
        
        return results
    except Exception as e:
        logger.error(f"Topic processing error: {e}")
        return results

def extract_batch(batch_id: str, progress_callback: Optional[Callable] = None) -> Optional[Any]:
    """Extract all content from a batch"""
    start_time = time.time()
    
    batch = get_batch_info(batch_id)
    if not batch:
        logger.error(f"Batch {batch_id} not found")
        return None
    
    batch_name = batch.get("batch_name") or batch.get("name") or f"Batch_{batch_id}"
    topics = batch.get("topics", [])
    
    if not topics:
        class EmptyStats:
            pass
        stats = EmptyStats()
        stats.batch_name = batch_name
        stats.total_items = 0
        stats.videos = 0
        stats.pdfs = 0
        stats.drm_count = 0
        stats.time_taken = time.time() - start_time
        stats.items = []
        return stats
    
    all_items = []
    videos = pdfs = drm = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_topic, batch_id, t) for t in topics]
        completed = 0
        total = len(topics)
        
        for future in as_completed(futures):
            completed += 1
            items = future.result()
            all_items.extend(items)
            
            for item in items:
                if item['type'] == 'video':
                    videos += 1
                elif item['type'] == 'pdf':
                    pdfs += 1
                else:
                    drm += 1
            
            if progress_callback and total > 0:
                percent = (completed / total) * 100
                bar = '█' * int(percent/5) + '░' * (20 - int(percent/5))
                progress_callback(
                    f"{EMOJI['video']} Videos: {videos} | {EMOJI['pdf']} PDFs: {pdfs}\n"
                    f"Progress: {bar} {percent:.1f}%"
                )
    
    class Stats:
        pass
    stats = Stats()
    stats.batch_name = batch_name
    stats.total_items = len(all_items)
    stats.videos = videos
    stats.pdfs = pdfs
    stats.drm_count = drm
    stats.time_taken = time.time() - start_time
    stats.items = all_items
    
    return stats

def validate_batch_id(batch_id: str) -> bool:
    """Validate if batch ID exists"""
    return get_batch_info(batch_id) is not None

# Cleanup
import atexit
atexit.register(lambda: session.close())
