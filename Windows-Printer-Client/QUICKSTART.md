# Quick Start Guide

## Start the Application

### Option 1: Using the Batch File (Easiest)
Double-click `start_printer_client.bat`

### Option 2: Using Command Line
```bash
cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
venv\Scripts\activate
python printer_client.py
```

## Before First Run

1. **Configure the application**
   - Open `.env` file
   - Update `SOCKET_URL` to your Backend-Socket server URL (default: http://localhost:5001)
   - Update `NIPT` with your company NIPT value
   - Optionally set `DEFAULT_PRINTER` or leave blank to use system default

2. **Ensure Backend-Socket is running**
   ```bash
   cd c:\Users\user\Desktop\ParidBackend\Backend-Socket
   # Start your Backend-Socket server
   ```

3. **Test your printer**
   ```bash
   cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
   venv\Scripts\activate
   python printer_test.py
   ```

## How It Works

1. Application connects to Backend-Socket server via WebSocket
2. Listens for print requests from the server
3. Automatically prints when requests are received
4. Sends confirmation back to server

## Testing from Backend-Socket

To test printing, emit a WebSocket event from your Backend-Socket server:

```python
from socketio_instance import socketio

# Emit a print request
socketio.emit('print_request', {
    'data': {
        'type': 'text',
        'document_name': 'Test Print',
        'content': 'Hello from Backend-Socket!\nThis is a test print.'
    }
})
```

## Troubleshooting

### Connection fails
- Check if Backend-Socket is running: http://localhost:5001
- Verify `.env` configuration
- Check firewall settings

### Printer not working
- Run `python printer_test.py` to test printer
- Check Windows printer settings
- Verify printer is turned on and connected

### Import errors
- Ensure virtual environment is activated
- Re-run: `venv\Scripts\pip.exe install -r requirements.txt`

## Logs

Check `printer_client.log` for detailed logs:
```bash
type printer_client.log
```

## Stop the Application

Press `Ctrl+C` in the terminal window
