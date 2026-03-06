# ==================== PROGRESS AND STATS CLASSES ====================

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
