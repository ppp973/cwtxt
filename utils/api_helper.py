import requests
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import BATCH_API, TOPIC_API, VIDEO_API, ALL_BATCHES_API, MAX_WORKERS, TIMEOUT

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session for reuse
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
})

def fetch_json(url, retries=3):
    """Fetch JSON from URL with retry mechanism"""
    for attempt in range(retries):
        try:
            logger.info(f"📡 Fetching: {url[:50]}...")
            response = session.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                logger.info(f"✅ Success: {url[:50]}...")
                return response.json()
            else:
                logger.warning(f"⚠️ Attempt {attempt+1}/{retries}: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.warning(f"⏰ Timeout attempt {attempt+1}/{retries}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"🔌 Connection error attempt {attempt+1}/{retries}")
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
        
        if attempt < retries - 1:
            time.sleep(2)  # Wait before retry
    
    logger.error(f"❌ Failed after {retries} attempts: {url[:50]}...")
    return None

def get_video_url(video_id):
    """Get actual video URL from video ID"""
    try:
        data = fetch_json(VIDEO_API.format(video_id))
        if data and isinstance(data, dict):
            # Try different response structures
            if "data" in data and "link" in data["data"]:
                return data["data"]["link"].get("file_url")
            elif "file_url" in data:
                return data["file_url"]
            elif "url" in data:
                return data["url"]
        return None
    except Exception as e:
        logger.error(f"Video fetch error: {str(e)}")
        return None

def get_batch_info(batch_id):
    """Get batch information"""
    return fetch_json(BATCH_API.format(batch_id))

def get_topic_details(batch_id, topic_id):
    """Get topic details with full content"""
    return fetch_json(TOPIC_API.format(batch_id, topic_id))

def get_all_batches():
    """Get all available batches"""
    return fetch_json(ALL_BATCHES_API)

def process_topic(batch_id, topic, progress_callback=None):
    """Process a single topic and extract all content"""
    try:
        topic_id = topic["id"]
        topic_name = topic.get("topicName", topic.get("name", "Unknown Topic"))
        
        if progress_callback:
            progress_callback(f"📥 Processing: {topic_name[:30]}...")
        
        topic_data = get_topic_details(batch_id, topic_id)
        
        if not topic_data:
            return []
        
        results = []
        
        # Extract videos
        classes = topic_data.get("classes", [])
        for cls in classes:
            title = cls.get("title", "Untitled Class")
            class_no = cls.get("class_no", "")
            video_id = cls.get("video_url")
            
            if video_id:
                video_url = get_video_url(video_id)
                if video_url:
                    results.append({
                        "type": "video",
                        "topic": topic_name,
                        "class_no": class_no,
                        "title": title,
                        "url": video_url,
                        "line": f"[{topic_name}] Class {class_no} | {title}: {video_url}"
                    })
        
        # Extract PDFs
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

def extract_batch(batch_id, progress_callback=None):
    """Extract all content from a batch"""
    start_time = time.time()
    
    # Get batch info
    batch = get_batch_info(batch_id)
    
    if not batch:
        return None
    
    batch_name = batch.get("batch_name", batch.get("name", f"Batch_{batch_id}"))
    topics = batch.get("topics", [])
    
    if not topics:
        return {
            "batch_id": batch_id,
            "batch_name": batch_name,
            "items": [],
            "videos": 0,
            "pdfs": 0,
            "total": 0,
            "time": 0
        }
    
    all_items = []
    videos_count = 0
    pdfs_count = 0
    
    # Process topics in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for topic in topics:
            future = executor.submit(process_topic, batch_id, topic, progress_callback)
            futures.append(future)
        
        completed = 0
        total = len(futures)
        
        for future in as_completed(futures):
            completed += 1
            results = future.result()
            
            if results:
                for item in results:
                    all_items.append(item["line"])
                    if item["type"] == "video":
                        videos_count += 1
                    else:
                        pdfs_count += 1
            
            if progress_callback:
                progress_callback(f"📊 Progress: {completed}/{total} topics completed")
    
    elapsed_time = time.time() - start_time
    
    return {
        "batch_id": batch_id,
        "batch_name": batch_name,
        "items": all_items,
        "videos": videos_count,
        "pdfs": pdfs_count,
        "total": len(all_items),
        "time": round(elapsed_time, 2)
    }
