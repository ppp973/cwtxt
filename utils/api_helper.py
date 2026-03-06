import requests
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Callable, Any
from config import MAX_WORKERS, TIMEOUT, MAX_RETRIES, RETRY_DELAY, EMOJI

logger = logging.getLogger(__name__)

# API Endpoints
BATCH_API_ENDPOINTS = [
    "https://cw-api-website.vercel.app/batch/{}",
    "https://api.careerwill.com/batch/{}"
]

TOPIC_API_ENDPOINTS = [
    "https://cw-api-website.vercel.app/batch?batchid={}&topicid={}&full=true",
    "https://api.careerwill.com/topic?batch={}&topic={}"
]

VIDEO_API_ENDPOINTS = [
    "https://cw-vid-virid.vercel.app/get_video_details?name={}",
    "https://api.careerwill.com/video/{}"
]

ALL_BATCHES_ENDPOINTS = [
    "https://cw-api-website.vercel.app/batches",
    "https://api.careerwill.com/batches"
]

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def fetch_json(urls: list, retries: int = MAX_RETRIES) -> Optional[Dict]:
    for url in urls:
        for attempt in range(retries):
            try:
                response = session.get(url, timeout=TIMEOUT)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    time.sleep(RETRY_DELAY * (attempt + 1) * 2)
            except:
                pass
            time.sleep(RETRY_DELAY)
    return None

def get_video_url(video_id: str) -> Optional[str]:
    try:
        data = fetch_json([api.format(video_id) for api in VIDEO_API_ENDPOINTS])
        if data:
            if "file_url" in data:
                return data["file_url"]
            if "data" in data and isinstance(data["data"], dict):
                if "link" in data["data"]:
                    return data["data"]["link"].get("file_url")
        return None
    except:
        return None

def get_batch_info(batch_id: str) -> Optional[Dict]:
    return fetch_json([api.format(batch_id) for api in BATCH_API_ENDPOINTS])

def get_topic_details(batch_id: str, topic_id: str) -> Optional[Dict]:
    return fetch_json([api.format(batch_id, topic_id) for api in TOPIC_API_ENDPOINTS])

def get_all_batches() -> Optional[Dict[str, str]]:
    return fetch_json(ALL_BATCHES_ENDPOINTS)

def validate_batch_id(batch_id: str) -> bool:
    return get_batch_info(batch_id) is not None

def process_topic(batch_id: str, topic: Dict) -> List[Dict]:
    results = []
    try:
        topic_id = topic.get("id") or topic.get("topicId")
        topic_name = topic.get("topicName") or topic.get("name") or "Unknown"
        
        if not topic_id:
            return results
        
        topic_data = get_topic_details(batch_id, topic_id)
        if not topic_data:
            return results
        
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
    except:
        return results

def extract_batch(batch_id: str, progress_callback: Optional[Callable] = None) -> Optional[Any]:
    start_time = time.time()
    
    batch = get_batch_info(batch_id)
    if not batch:
        return None
    
    batch_name = batch.get("batch_name") or batch.get("name") or f"Batch_{batch_id}"
    topics = batch.get("topics", [])
    
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

class ExtractionProgress:
    def __init__(self, total_topics):
        self.total_topics = total_topics
        self.completed_topics = 0
        self.total_videos = 0
        self.total_pdfs = 0

class ExtractionStats:
    def __init__(self, batch_id, batch_name, total_items, videos, pdfs, drm_count, time_taken, topics_processed, failed_topics, success_rate):
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

import atexit
atexit.register(lambda: session.close())
