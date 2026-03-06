# ये क्लासेस फाइल के अंत में होनी चाहिए (imports के बाद)

class ExtractionProgress:
    """Progress tracking for extraction"""
    def __init__(self, total_topics):
        self.total_topics = total_topics
        self.completed_topics = 0
        self.total_videos = 0
        self.total_pdfs = 0
        self.current_topic = ""
        self.start_time = __import__('time').time()
        self.estimated_time = 0
    
    def update(self, topic_name, videos=0, pdfs=0):
        self.completed_topics += 1
        self.current_topic = topic_name
        self.total_videos += videos
        self.total_pdfs += pdfs
        
        elapsed = __import__('time').time() - self.start_time
        if self.completed_topics > 0:
            avg_time = elapsed / self.completed_topics
            remaining = self.total_topics - self.completed_topics
            self.estimated_time = avg_time * remaining
    
    def get_percentage(self):
        if self.total_topics == 0:
            return 0
        return (self.completed_topics / self.total_topics) * 100

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
        self.items = []  # Will store actual items
