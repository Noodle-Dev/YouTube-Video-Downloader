class DownloadModel:
    def __init__(self):
        self.download_history = []
    
    def add_to_history(self, url, platform, path, status):
        self.download_history.append({
            'url': url,
            'platform': platform,
            'path': path,
            'status': status,
            'timestamp': datetime.now()
        })
    
    def get_history(self):
        return self.download_history
    
    def clear_history(self):
        self.download_history = []