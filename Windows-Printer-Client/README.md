# Print Client Pro

Professional Windows Printer Client Service for Background Printing

## Overview

Print Client Pro is a background service that enables seamless printer management and automatic print job handling on Windows systems. It runs silently in the system tray and maintains a persistent connection to your print server.

## Features

- **Background Service**: Runs continuously in the Windows system tray
- **Auto-Start**: Automatically starts when Windows boots
- **Real-time Printing**: Receives and processes print jobs via WebSocket connection
- **Queue Management**: Manages failed print jobs with retry functionality
- **Printer Configuration**: Easy printer setup and management
- **Multiple Print Types**: Supports text, HTML (with PDF conversion), and document printing
- **HTML to PDF Conversion**: Automatically converts HTML receipts to PDF for high-quality printing
- **Thermal Printer Support**: Optimized for 80mm thermal receipt printers
- **Spooler Integration**: Direct integration with Windows Print Spooler
- **Professional GUI**: Modern, intuitive interface for monitoring and configuration

## Installation

1. Run the installer: `PrintClientPro_Setup_v1.0.0.exe`
2. Follow the installation wizard
3. Enter your configuration during setup:
   - Socket Server URL
   - NIPT (Company ID)
   - Username
   - Session ID
4. Choose whether to start automatically with Windows
5. Click Install

## Usage

### First Run
After installation, Print Client Pro will start automatically. Look for the printer icon in your system tray (bottom-right corner of screen).

### Opening the Application
- **Left-click** or **double-click** the tray icon to open the GUI
- **Right-click** the tray icon for quick menu

### System Tray Menu
- **Show Window**: Open the application GUI
- **Hide Window**: Hide the GUI (app continues running)
- **Exit**: Completely close the application

### Main Interface
The application has three main views:

1. **Console Log**: View real-time activity and print job status
2. **Print Queue**: See pending print jobs and manage retries
3. **Printers**: Configure and manage your printers

### Configuration
Click the **Configuration** button in the sidebar to:
- Update Socket Server URL
- Change NIPT/Username/Session ID
- Save configuration changes

### Printing
Print jobs are automatically received from the server and processed in the background. You can:
- Monitor print status in the Console Log
- View queued jobs in the Print Queue
- Retry failed print jobs
- Cancel pending prints

#### HTML Printing Support
The client now supports **high-quality HTML printing** with automatic PDF conversion:

**Supported Data Format:**
```json
{
  "printer_name": "Your Printer Name",
  "content": "<!DOCTYPE html><html>...your HTML content...</html>",
  "type": "html"  // Optional - auto-detected if content starts with HTML
}
```

**How it works:**
1. HTML content is received from the server
2. The client automatically detects HTML and converts it to PDF
3. PDF is optimized for 80mm thermal receipt printers
4. The formatted PDF is sent to the specified printer
5. All styling, tables, and formatting are preserved

**Features:**
- Automatic HTML detection (no need to specify type if HTML starts with `<!DOCTYPE html>`)
- Supports full CSS styling from your HTML
- Optimized for thermal receipt printers (80mm width)
- Tables, borders, and custom fonts are properly rendered
- Falls back to text-only printing if PDF conversion fails

**Example HTML Receipt:**
```json
{
  "printer_name": "Thermal Printer",
  "content": "<!DOCTYPE html><html><head><style>table{width:100%}...</style></head><body><table>...receipt content...</table></body></html>"
}
```

## System Requirements

- Windows 10 or later
- Internet connection for WebSocket server communication
- At least one printer installed on the system
- Python dependencies (automatically installed):
  - weasyprint (for HTML to PDF conversion)
  - reportlab (fallback PDF generator)
  - beautifulsoup4 (HTML parsing)
  - pywin32 (Windows API access)

## Troubleshooting

### Application Not Starting
1. Check if the application is already running in the system tray
2. Look for the printer icon near the clock
3. Try restarting your computer

### Cannot Connect to Server
1. Verify the Socket Server URL in configuration
2. Check your internet connection
3. Ensure the print server is running
4. Check firewall settings

### Print Jobs Not Processing
1. Verify printer is installed and online
2. Check Windows Print Spooler service is running
3. Review error logs in the Console Log view
4. Try a test print from the application

### Failed Print Jobs
Failed jobs are automatically added to the queue. You can:
- Click **Retry** to attempt printing again
- Click **Delete** to remove from queue
- Click **Show** to preview the print content

## Configuration Files

Print Client Pro stores configuration in the installation directory:

- `.env`: Server connection settings
- `printer_settings.json`: Printer configurations
- `printer_client_gui.log`: Application logs

## Uninstallation

1. Right-click the tray icon and select **Exit**
2. Go to Windows Settings > Apps > Installed Apps
3. Find "Print Client Pro" and click Uninstall
4. Follow the uninstallation wizard

Configuration files and logs will be automatically removed.

## Support

For technical support, updates, and documentation:
- Website: https://www.printclientpro.com
- Email: support@printclientpro.com

## Version History

### Version 1.0.0 (2025)
- Initial release
- Background service with system tray
- WebSocket connection to print server
- Queue management
- Printer configuration
- Auto-start functionality

## License

Copyright (c) 2025 Print Client Pro. All rights reserved.
See LICENSE.txt for full license terms.
