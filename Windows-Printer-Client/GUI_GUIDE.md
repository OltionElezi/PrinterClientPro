# Windows Printer Client - GUI Application Guide

## 🎨 Desktop GUI Application

The Windows Printer Client now has a **graphical desktop application** with a visual interface!

## 🚀 How to Start the GUI

### Option 1: Double-Click (Easiest)
```
Double-click: start_gui.bat
```

### Option 2: Command Line
```bash
cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
venv\Scripts\python.exe printer_client_gui.py
```

## 📸 GUI Features

### Left Panel - Configuration
- **Socket Server URL**: Backend-Socket server address
- **NIPT**: Your company NIPT (can be edited in real-time)
- **Username**: Client username for authentication
- **Session ID**: Unique session identifier
- **Printer**: Select from available printers dropdown

### Connection Controls
- **💾 Save Configuration**: Save settings to .env file
- **🔌 Connect/Disconnect**: Toggle connection to server
- **🖨️ Test Print**: Send a test print to verify printer works
- **Status Indicator**: Shows connection status
  - 🔴 Red = Disconnected
  - 🟢 Green = Connected

### Right Panel - Activity Log
- **Real-time Log Display**: Shows all events, messages, and errors
- **Color-Coded Messages**:
  - 🔵 Blue = Info messages
  - 🟡 Yellow = Warnings
  - 🔴 Red = Errors
- **🗑️ Clear Log**: Clear the log display
- **Statistics**: Track print count and errors

## 📋 How to Use

### 1. Configure Settings
1. Enter your **NIPT** value
2. Verify **Socket Server URL** (default: http://127.0.0.1:5001)
3. Select your **Printer** from dropdown
4. Click **💾 Save Configuration**

### 2. Connect to Server
1. Make sure Backend-Socket server is running
2. Click **🔌 Connect** button
3. Watch the Activity Log for connection status
4. Status indicator will turn 🟢 Green when connected

### 3. Test Printing
1. Once connected, click **🖨️ Test Print**
2. Check your printer for output
3. Monitor the Activity Log for print status

### 4. Monitor Activity
- All WebSocket messages appear in the Activity Log
- Print requests show details: type, printer, status
- Errors are highlighted in red
- Statistics show total prints and errors

## 🎯 GUI Window Layout

```
┌─────────────────────────────────────────────────────────┐
│        🖨️ Windows Printer Client                       │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│ Configuration│        Activity Log                      │
│              │                                          │
│ [Settings]   │  [Real-time messages]                   │
│ [Printer]    │  • Connection events                    │
│              │  • Print requests                       │
│ Status: ●    │  • Errors & warnings                    │
│ Disconnected │  • Socket messages                      │
│              │                                          │
│ [Connect]    │  [Clear Log]                            │
│ [Test Print] │  Stats: Prints: 0  Errors: 0            │
└──────────────┴──────────────────────────────────────────┘
```

## 🔧 Configuration Fields

| Field | Description | Example |
|-------|-------------|---------|
| Socket Server URL | Backend-Socket server address | http://127.0.0.1:5001 |
| NIPT | Company tax identifier | PSSTEST |
| Username | Client username | printer_client |
| Session ID | Unique session ID | printer_client_session_001 |
| Printer | Selected Windows printer | RONGTA 80mm Series Printer |

## 📝 Activity Log Messages

### Connection Events
```
✅ Successfully connected to Backend-Socket server
📨 Status: Printer client connected and joined room
⚠️ Disconnected from server
```

### Print Events
```
🖨️ Print request received
   Type: receipt
   Printer: RONGTA 80mm Series Printer
✅ Print job completed successfully
```

### Errors
```
❌ Connection failed: Connection refused
❌ Print job failed
❌ Error processing print: Invalid data
```

## 🎨 Color Coding

The Activity Log uses color coding for easy identification:
- **Blue (Info)**: Normal operations, status messages
- **Yellow (Warning)**: Warnings, disconnections
- **Red (Error)**: Errors, failed operations

## 💾 Saving Configuration

When you click "💾 Save Configuration":
- All settings are saved to `.env` file
- Configuration persists between sessions
- Confirmation message appears

## 🧪 Test Print

The "🖨️ Test Print" button:
- Only enabled when connected
- Sends a test document to selected printer
- Shows timestamp and connection info
- Useful for verifying printer setup

## 🔄 Auto-Reconnect

The GUI handles disconnections gracefully:
- Shows warning when connection lost
- Manual reconnect via Connect button
- Activity log shows all reconnection attempts

## 📊 Statistics

Bottom of the log panel shows:
- **Prints**: Total successful print jobs
- **Errors**: Total errors encountered
- Resets when application restarts

## 🚪 Closing the Application

When closing the window:
- If connected, asks for confirmation
- Automatically disconnects from server
- Saves current state

## 🆚 GUI vs Console Version

| Feature | GUI | Console |
|---------|-----|---------|
| Visual Interface | ✅ Yes | ❌ No |
| Real-time Configuration | ✅ Yes | ❌ No |
| Log Display | ✅ Colored | ⚠️ Plain text |
| NIPT Configuration | ✅ Easy | ⚠️ Edit .env file |
| Connection Status | ✅ Visual | ⚠️ Text only |
| Statistics | ✅ Yes | ❌ No |
| Test Print Button | ✅ Yes | ❌ No |

## 📂 Files

- **printer_client_gui.py**: GUI application source code
- **start_gui.bat**: Quick start batch file
- **printer_client_gui.log**: Application log file (UTF-8)
- **.env**: Configuration file (editable in GUI)

## 🔍 Troubleshooting

### GUI doesn't appear
- Check if Python is installed: `python --version`
- Verify virtual environment: `venv\Scripts\python.exe --version`
- Check for errors in console

### Can't connect
- Ensure Backend-Socket is running on specified URL
- Check NIPT value is correct
- Verify firewall settings
- Check Activity Log for error messages

### Printer not working
- Use Test Print button to verify
- Check printer is powered on
- Verify printer selection in dropdown
- Check Windows printer settings

## 💡 Tips

1. **Keep GUI Open**: Leave the application running to receive print requests
2. **Monitor Logs**: Watch Activity Log for real-time status
3. **Save Configuration**: Always save after changing NIPT or printer settings
4. **Test First**: Use Test Print before relying on automatic printing
5. **Check Statistics**: Monitor print count to ensure requests are received

## 🎯 Next Steps

1. Start the GUI application
2. Configure your NIPT value
3. Connect to Backend-Socket server
4. Test printing
5. Monitor activity in real-time

The GUI provides a much better user experience than the console version!
