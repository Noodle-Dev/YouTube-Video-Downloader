from PyQt5.QtWidgets import (QMainWindow, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QWidget, QComboBox, QFileDialog, 
                            QMessageBox, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from controllers.download_controller import DownloadController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_controller = DownloadController()
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        self.setWindowTitle("Universal Video Downloader")
        self.setFixedSize(550, 400)
        self.load_styles()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        self.create_header()
        self.create_url_section()
        self.create_platform_section()
        self.create_path_section()
        self.create_progress_bar()
        self.create_download_button()
        self.create_status_label()
        
        self.central_widget.setLayout(self.main_layout)
    
    def setup_connections(self):
        self.path_button.clicked.connect(self.select_directory)
        self.download_button.clicked.connect(self.start_download)
    
    def load_styles(self):
        # Styles would be loaded from external CSS file in production
        self.setStyleSheet("""
            /* Dark theme styles here */
        """)
    
    def create_header(self):
        self.header = QLabel("Universal Video Downloader")
        self.header.setFont(QFont("Arial", 16, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("color: #4CAF50; margin-bottom: 10px;")
        self.main_layout.addWidget(self.header)
    
    # Other UI creation methods here...
    
    def select_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_path = folder
            self.path_display.setText(folder)
    
    def start_download(self):
        url = self.url_input.text().strip()
        platform = self.platform_combo.currentText()
        self.download_controller.start_download(url, platform, self.download_path)