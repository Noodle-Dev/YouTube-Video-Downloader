import os
import pytube
from yt_dlp import YoutubeDL
from PyQt5.QtWidgets import QMessageBox

class DownloadController:
    def __init__(self, view=None):
        self.view = view
    
    def start_download(self, url, platform, download_path):
        if not url:
            self.show_error("Please enter a valid URL")
            return
        
        if not download_path:
            self.show_error("Please select a download folder")
            return
        
        try:
            if platform == "YouTube":
                self.download_youtube(url, download_path)
            else:
                self.download_other(url, download_path, platform)
            
            self.show_success("Download completed successfully!")
        
        except Exception as e:
            self.show_error(f"An error occurred:\n{str(e)}")
    
    def download_youtube(self, url, download_path):
        video = pytube.YouTube(url)
        stream = video.streams.get_highest_resolution()
        stream.download(output_path=download_path)
    
    def download_other(self, url, download_path, platform):
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
    
    def show_error(self, message):
        QMessageBox.critical(self.view, "Error", message)
    
    def show_success(self, message):
        QMessageBox.information(self.view, "Success", message)