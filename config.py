import os

class Config:
    DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    SECRET_KEY = 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB limit