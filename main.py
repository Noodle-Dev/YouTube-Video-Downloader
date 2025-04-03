import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QWidget, QComboBox,
                             QFileDialog, QMessageBox, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
import pytube
from yt_dlp import YoutubeDL

class VideoDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Downloader")
        self.setFixedSize(550, 400)
        
        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D;
            }
            QLabel {
                color: #E0E0E0;
            }
            QLineEdit, QComboBox {
                background-color: #3D3D3D;
                color: #FFFFFF;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                selection-background-color: #555;
            }
            QPushButton {
                background-color: #444;
                color: #FFF;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
            QPushButton#downloadButton {
                background-color: #4CAF50;
                font-weight: bold;
            }
            QPushButton#downloadButton:hover {
                background-color: #5CBF60;
            }
            QPushButton#downloadButton:pressed {
                background-color: #3C9F40;
            }
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                text-align: center;
                background-color: #3D3D3D;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Header
        self.header = QLabel("YT Download")
        self.header.setFont(QFont("Arial", 16, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("color: #4CAF50; margin-bottom: 10px;")
        self.main_layout.addWidget(self.header)
        
        # URL Section
        self.url_layout = QVBoxLayout()
        self.url_label = QLabel("Video URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.url_layout.addWidget(self.url_label)
        self.url_layout.addWidget(self.url_input)
        self.main_layout.addLayout(self.url_layout)
        
        # Platform Section
        self.platform_layout = QHBoxLayout()
        self.platform_label = QLabel("Platform:")
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["YouTube", "TikTok", "Twitter", "Instagram", "Other"])
        self.platform_combo.setItemIcon(0, QIcon("icons/youtube.png"))
        self.platform_combo.setItemIcon(1, QIcon("icons/tiktok.png"))
        self.platform_combo.setItemIcon(2, QIcon("icons/twitter.png"))
        self.platform_combo.setItemIcon(3, QIcon("icons/instagram.png"))
        self.platform_combo.setItemIcon(4, QIcon("icons/video.png"))
        self.platform_layout.addWidget(self.platform_label)
        self.platform_layout.addWidget(self.platform_combo)
        self.main_layout.addLayout(self.platform_layout)
        
        # Path Section
        self.path_layout = QVBoxLayout()
        self.path_label = QLabel("Download Folder:")
        self.path_button = QPushButton("Select Folder")
        self.path_button.setObjectName("pathButton")
        self.path_button.clicked.connect(self.select_directory)
        self.path_display = QLabel("No folder selected")
        self.path_display.setStyleSheet("color: #AAA; font-style: italic;")
        self.path_layout.addWidget(self.path_label)
        self.path_layout.addWidget(self.path_button)
        self.path_layout.addWidget(self.path_display)
        self.main_layout.addLayout(self.path_layout)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.main_layout.addWidget(self.progress_bar)
        
        # Download Button
        self.download_button = QPushButton("Download Video")
        self.download_button.setObjectName("downloadButton")
        self.download_button.setIcon(QIcon("icons/download.png"))
        self.download_button.setIconSize(QSize(16, 16))
        self.download_button.clicked.connect(self.start_download)
        self.main_layout.addWidget(self.download_button)
        
        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #AAA; font-style: italic;")
        self.main_layout.addWidget(self.status_label)
        
        # Variables
        self.download_path = ""
        self.central_widget.setLayout(self.main_layout)
    
    def select_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_path = folder
            self.path_display.setText(folder)
            self.path_display.setStyleSheet("color: #E0E0E0; font-style: normal;")
    
    def update_progress(self, stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        progress = int((bytes_downloaded / file_size) * 100)
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"Downloading... {progress}%")
        QApplication.processEvents()
    
    def start_download(self):
        url = self.url_input.text().strip()
        platform = self.platform_combo.currentText()
        
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL")
            return
        
        if not self.download_path:
            QMessageBox.warning(self, "Error", "Please select a download folder")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Preparing download...")
        self.download_button.setEnabled(False)
        QApplication.processEvents()
        
        try:
            if platform == "YouTube":
                video = pytube.YouTube(
                    url,
                    on_progress_callback=self.update_progress,
                    on_complete_callback=self.download_complete
                )
                stream = video.streams.get_highest_resolution()
                self.status_label.setText(f"Downloading: {video.title}")
                stream.download(output_path=self.download_path)
            else:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.yt_dlp_progress],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    self.status_label.setText(f"Downloaded: {info.get('title', 'video')}")
            
            QMessageBox.information(self, "Success", "Download completed successfully!")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.progress_bar.setVisible(False)
            self.download_button.setEnabled(True)
            self.status_label.setText("Ready")
    
    def yt_dlp_progress(self, d):
        if d['status'] == 'downloading':
            progress = int(float(d['_percent_str'].replace('%', '')))
            self.progress_bar.setValue(progress)
            self.status_label.setText(
                f"Downloading... {d['_percent_str']} at {d['_speed_str']}"
            )
            QApplication.processEvents()
    
    def download_complete(self, stream, file_path):
        self.progress_bar.setValue(100)
        self.status_label.setText("Download complete!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set dark palette
    dark_palette = app.palette()
    dark_palette.setColor(dark_palette.Window, Qt.darkGray)
    dark_palette.setColor(dark_palette.WindowText, Qt.white)
    dark_palette.setColor(dark_palette.Base, Qt.darkGray)
    dark_palette.setColor(dark_palette.AlternateBase, Qt.gray)
    dark_palette.setColor(dark_palette.ToolTipBase, Qt.white)
    dark_palette.setColor(dark_palette.ToolTipText, Qt.white)
    dark_palette.setColor(dark_palette.Text, Qt.white)
    dark_palette.setColor(dark_palette.Button, Qt.darkGray)
    dark_palette.setColor(dark_palette.ButtonText, Qt.white)
    dark_palette.setColor(dark_palette.BrightText, Qt.red)
    dark_palette.setColor(dark_palette.Link, Qt.cyan)
    dark_palette.setColor(dark_palette.Highlight, Qt.darkCyan)
    dark_palette.setColor(dark_palette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    window = VideoDownloaderApp()
    window.show()
    sys.exit(app.exec_())