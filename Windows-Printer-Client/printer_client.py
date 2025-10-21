"""
Windows Printer Client
Connects to Backend-Socket via WebSocket and handles print requests
"""
import socketio
import time
import json
import logging
from datetime import datetime
from printer_handler import PrinterHandler
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('printer_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PrinterClient:
    def __init__(self):
        self.config = Config()
        self.sio = socketio.Client(logger=True, engineio_logger=True)
        self.printer_handler = PrinterHandler()
        self.connected = False
        self.setup_event_handlers()

    def setup_event_handlers(self):
        """Setup WebSocket event handlers"""

        @self.sio.event
        def connect():
            self.connected = True
            logger.info("Successfully connected to Backend-Socket server")
            logger.info(f"Client ID: {self.sio.sid}")

        @self.sio.event
        def connect_error(data):
            logger.error(f"Connection failed: {data}")
            self.connected = False

        @self.sio.event
        def disconnect():
            self.connected = False
            logger.warning("Disconnected from server")

        @self.sio.on('status')
        def on_status(data):
            logger.info(f"Status update: {data}")

        @self.sio.on('print_request')
        def on_print_request(data):
            """Handle incoming print requests"""
            logger.info(f"Received print request: {data}")
            try:
                # Extract print data - handle different data structures
                if 'data' in data:
                    print_data = data.get('data', {})
                else:
                    print_data = data

                # Get printer name
                printer_name = data.get('printer_name', self.config.DEFAULT_PRINTER)

                # Auto-detect HTML content
                content = print_data.get('content', '')
                if content and isinstance(content, str):
                    # Check if content is HTML
                    if content.strip().startswith('<!DOCTYPE html>') or content.strip().startswith('<html'):
                        # Set type to html if not already set
                        if 'type' not in print_data:
                            print_data['type'] = 'html'
                            logger.info("Auto-detected HTML content")

                # Process the print request
                result = self.printer_handler.print_document(print_data, printer_name)

                # Send acknowledgment back to server
                self.sio.emit('print_response', {
                    'status': 'success' if result else 'failed',
                    'message': 'Print job sent successfully' if result else 'Print job failed',
                    'timestamp': datetime.now().isoformat(),
                    'printer': printer_name
                })

            except Exception as e:
                logger.error(f"Error processing print request: {str(e)}")
                self.sio.emit('print_response', {
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                })

        @self.sio.on('pos')
        def on_pos_update(data):
            """Handle POS updates that may trigger printing"""
            logger.info(f"Received POS update: {data}")
            pos_data = data.get('pos_data', {})

            # Check if this POS update requires printing
            if pos_data.get('print_required'):
                self.printer_handler.print_receipt(pos_data)

        @self.sio.on('reservation')
        def on_reservation_update(data):
            """Handle reservation updates that may trigger printing"""
            logger.info(f"Received reservation update: {data}")
            reservation_data = data.get('reservation_data', {})

            # Check if this reservation requires printing
            if reservation_data.get('print_required'):
                self.printer_handler.print_reservation(reservation_data)

    def connect_to_server(self):
        """Connect to the Backend-Socket server"""
        try:
            # Build connection URL with query parameters
            url = f"{self.config.SOCKET_URL}?session_id={self.config.SESSION_ID}&username={self.config.USERNAME}&nipt={self.config.NIPT}"

            logger.info(f"Connecting to {self.config.SOCKET_URL}...")
            self.sio.connect(url, transports=['websocket'])

            logger.info("Connection established!")
            return True

        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            return False

    def disconnect_from_server(self):
        """Disconnect from the server"""
        if self.connected:
            self.sio.disconnect()
            logger.info("Disconnected from server")

    def run(self):
        """Main run loop"""
        logger.info("Starting Windows Printer Client...")
        logger.info(f"Configuration: {self.config.SOCKET_URL}")

        # Connect to server
        if not self.connect_to_server():
            logger.error("Failed to establish connection. Exiting...")
            return

        try:
            # Keep the client running
            logger.info("Client is running. Press Ctrl+C to stop...")
            while True:
                time.sleep(1)

                # Check connection status
                if not self.connected:
                    logger.warning("Connection lost. Attempting to reconnect...")
                    time.sleep(5)  # Wait before reconnecting
                    self.connect_to_server()

        except KeyboardInterrupt:
            logger.info("Shutting down printer client...")
            self.disconnect_from_server()
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            self.disconnect_from_server()

def main():
    """Main entry point"""
    client = PrinterClient()
    client.run()

if __name__ == "__main__":
    main()
