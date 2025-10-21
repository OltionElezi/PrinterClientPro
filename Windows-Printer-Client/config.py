"""
Configuration file for Windows Printer Client
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the printer client"""

    # WebSocket Server Configuration
    SOCKET_URL = os.getenv('SOCKET_URL', 'http://localhost:5001')

    # Authentication parameters (required by your Backend-Socket)
    SESSION_ID = os.getenv('SESSION_ID', 'printer_client_session_001')
    USERNAME = os.getenv('CLIENT_USERNAME', 'printer_client')
    NIPT = os.getenv('NIPT', 'default_nipt')

    # Printer Configuration
    DEFAULT_PRINTER = os.getenv('DEFAULT_PRINTER', None)  # None = use system default

    # PDF Converter Configuration
    PDF_CONVERTER = os.getenv('PDF_CONVERTER', 'reportlab')  # Options: 'reportlab', 'weasyprint', 'sumatrapdf', 'wkhtmltopdf'

    # Font Size Configuration (for ReportLab renderer)
    FONT_SCALE = float(os.getenv('FONT_SCALE', '0.8'))  # 0.8 = 20% smaller, 1.0 = normal, 1.2 = 20% larger

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'printer_client.log')

    # Reconnection settings
    RECONNECT_DELAY = int(os.getenv('RECONNECT_DELAY', '5'))  # seconds
    MAX_RECONNECT_ATTEMPTS = int(os.getenv('MAX_RECONNECT_ATTEMPTS', '0'))  # 0 = infinite

    def __repr__(self):
        return f"<Config SOCKET_URL={self.SOCKET_URL} USERNAME={self.USERNAME}>"
