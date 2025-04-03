import os
from pathlib import Path

class Config:
    # App info
    APP_NAME = "Video Downloader"
    VERSION = "1.0"
    
    # Supported platforms
    PLATFORMS = ["YouTube", "TikTok", "Twitter", "Instagram", "Other"]
    
    # Default paths
    BASE_DIR = Path(__file__).parent
    DOWNLOAD_DIR = str(Path.home() / "Downloads")
    ICON_DIR = str(BASE_DIR / "assets" / "icons")
    
    # UI settings
    WINDOW_SIZE = (600, 400)
    DARK_STYLE = """
        QMainWindow { background-color: #2D2D2D; }
        QLabel { color: #E0E0E0; }
        QLineEdit, QComboBox {
            background-color: #3D3D3D;
            color: #FFFFFF;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton {
            background-color: #444;
            color: #FFF;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 8px;
        }
        QPushButton:hover { background-color: #555; }
        QPushButton:pressed { background-color: #666; }
        #downloadBtn {
            background-color: #4CAF50;
            font-weight: bold;
        }
        QProgressBar {
            border: 1px solid #444;
            border-radius: 3px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
        }
    """