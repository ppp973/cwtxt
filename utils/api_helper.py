
"""
CareerWill Bot - API Helper Module
Handles all API calls to CareerWill servers.
"""

import requests
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Callable

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

# Session
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def fetch_json(url: str, retries: int = MAX_RETRIES) -> Optional[Dict]:
    """Fetch JSON from URL with retry mechanism"""
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    return None

def get_video_url(video_id: str) -> Optional[str]:
    """Get actual video URL from video ID"""
    data = fetch_json(VIDEO_API.format(video_id))
    if data and isinstance(data, dict):
        return data.get("file_url") or (data.get("data", {}).get("link", {}).get("file_url"))
    return None

def get_batch_info(batch_id: str) -> Optional[Dict]:
    """Get batch information"""
    return fetch_json(BATCH_API.format(batch_id))

def get_topic_details(batch_id: str, topic_id: str) -> Optional[Dict]:
    """Get topic details"""
    return fetch_json(TOPIC_API.format(batch_id, topic_id))

def get_all_batches() -> Optional[Dict[str, str]]:
    """Get all available batches"""
    return fetch_json(ALL_BATCHES_API)

def process_topic(batch_id: str, topic: Dict) -> List[Dict]:
    """Process a single topic"""
    results = []
    topic_id = topic.get("id")
    topic_name = topic.get("topicName", "Unknown")
    
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

def extract_batch(batch_id: str, progress_callback: Optional[Callable] = None):
    """Extract all content from a batch"""
    start_time = time.time()
    batch = get_batch_info(batch_id)
    
    if not batch:
        return None
    
    batch_name = batch.get("batch_name", f"Batch_{batch_id}")
    topics = batch.get("topics", [])
    
    all_items = []
    videos = pdfs = drm = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_topic, batch_id, t) for t in topics]
        for i, future in enumerate(as_completed(futures)):
            items = future.result()
            all_items.extend(items)
            for item in items:
                if item['type'] == 'video': videos += 1
                elif item['type'] == 'pdf': pdfs += 1
                else: drm += 1
            if progress_callback:
                progress_callback(f"📊 Progress: {i+1}/{len(topics)} topics")
    
    class Stats:
        pass
    stats = Stats()
    stats.batch_id = batch_id
    stats.batch_name = batch_name
    stats.total_items = len(all_items)
    stats.videos = videos
    stats.pdfs = pdfs
    stats.drm_count = drm
    stats.time_taken = time.time() - start_time
    stats.items = all_items
    stats.topics_processed = len(topics)
    stats.success_rate = 100
    
    return stats

def validate_batch_id(batch_id: str) -> bool:
    """Validate if batch ID exists"""
    return get_batch_info(batch_id) is not None

__all__ = [
    'fetch_json', 'get_video_url', 'get_batch_info', 'get_topic_details',
    'get_all_batches', 'process_topic', 'extract_batch', 'validate_batch_id'
]
