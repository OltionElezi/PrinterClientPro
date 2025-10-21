"""
Printer Test Script
Tests the printer connection and basic printing functionality
"""
from printer_handler import PrinterHandler
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Test printer functionality"""
    logger.info("Starting printer test...")

    try:
        # Initialize printer handler
        handler = PrinterHandler()

        # Get available printers
        printers = handler.get_available_printers()
        logger.info(f"Available printers: {printers}")
        logger.info(f"Default printer: {handler.default_printer}")

        # Ask user if they want to test print
        print("\nAvailable printers:")
        for i, printer in enumerate(printers):
            print(f"{i + 1}. {printer}")

        print(f"\nDefault printer: {handler.default_printer}")

        response = input("\nDo you want to send a test print? (y/n): ")

        if response.lower() == 'y':
            logger.info("Sending test print...")
            result = handler.test_printer()

            if result:
                logger.info("Test print successful!")
                print("\nTest print sent successfully! Check your printer.")
            else:
                logger.error("Test print failed!")
                print("\nTest print failed. Check the logs for details.")
        else:
            logger.info("Test print skipped.")

    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
