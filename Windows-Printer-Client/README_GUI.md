# 🖨️ Windows Printer Client - Desktop GUI Application

A beautiful, user-friendly desktop application for managing printer connections to Backend-Socket server.

![Status](https://img.shields.io/badge/Status-Ready-green)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

## 🎨 What is This?

This is a **Windows desktop GUI application** that:
- Connects to your Backend-Socket server via WebSocket
- Receives print requests and sends them to your printer
- Provides a visual interface to monitor all activity
- Allows real-time configuration of settings (NIPT, printer, etc.)
- Shows colored logs, connection status, and statistics

**No more command line!** Everything is visual and easy to use.

## 🚀 Quick Start

### Step 1: Start the Application

**Double-click this file:**
```
start_gui.bat
```

That's it! The GUI window will appear.

### Step 2: Configure Settings

In the left panel:
1. Enter your **NIPT** value (your company identifier)
2. Verify **Socket Server URL** (default: http://127.0.0.1:5001)
3. Select your **Printer** from the dropdown
4. Click **💾 Save Configuration**

### Step 3: Connect

1. Make sure Backend-Socket server is running
2. Click **🔌 Connect** button
3. Watch the green ● indicator light up
4. Activity log will show: "✅ Successfully connected"

### Step 4: Test

Click **🖨️ Test Print** to verify everything works!

## 📸 Screenshot Description

```
┌──────────────────────────────────────────────────┐
│  🖨️ Windows Printer Client                      │
├─────────────────┬────────────────────────────────┤
│ Configuration   │  Activity Log                  │
│ ───────────────│  ──────────────────────────    │
│ Server URL:     │  15:30:45 - INFO - 🚀 Windows  │
│ [127.0.0.1:5001]│    Printer Client GUI started  │
│                 │  15:30:45 - INFO - 📍 Default  │
│ NIPT:           │    Printer: RONGTA 80mm Series │
│ [PSSTEST]       │  15:30:52 - INFO - 🔄 Connecting│
│                 │  15:30:53 - INFO - ✅ Successfully│
│ Username:       │    connected to Backend-Socket │
│ [printer_client]│  15:31:05 - INFO - 🖨️ Print    │
│                 │    request received            │
│ Session ID:     │  15:31:05 - INFO - ✅ Print job│
│ [printer_...]   │    completed successfully      │
│                 │                                │
│ Printer:        │  [🗑️ Clear Log]               │
│ [RONGTA 80mm ▼] │  Prints: 3  Errors: 0         │
│                 │                                │
│ [💾 Save Config]│                                │
│                 │                                │
│ Status          │                                │
│     ●           │                                │
│  Connected      │                                │
│ ID: E0RL6m...   │                                │
│                 │                                │
│ [🔌 Disconnect] │                                │
│ [🖨️ Test Print] │                                │
└─────────────────┴────────────────────────────────┘
```

## 🎯 Key Features

### ✅ Visual Configuration
- Change NIPT without editing files
- Select printer from dropdown
- Save configuration with one click
- All settings visible at a glance

### ✅ Real-Time Monitoring
- See all WebSocket messages live
- Color-coded logs (blue=info, yellow=warning, red=error)
- Connection status indicator (red=disconnected, green=connected)
- Print statistics (total prints, errors)

### ✅ Easy Controls
- Connect/Disconnect button
- Test Print button (verify printer works)
- Clear Log button
- Save Configuration button

### ✅ Professional Interface
- Clean, modern design
- Organized layout
- Scrollable logs
- Resizable window

## 🔧 Configuration

All settings are in the left panel:

| Setting | What it is | Example |
|---------|------------|---------|
| **Socket Server URL** | Your Backend-Socket address | http://127.0.0.1:5001 |
| **NIPT** | Company tax ID (important!) | PSSTEST |
| **Username** | Client username | printer_client |
| **Session ID** | Unique session ID | printer_client_session_001 |
| **Printer** | Windows printer to use | RONGTA 80mm Series Printer |

**Important:** Make sure to set the correct **NIPT** value for your company!

## 📝 Activity Log

The right panel shows all activity in real-time:

### Message Types

**Connection Events:**
```
🔄 Connecting to http://127.0.0.1:5001...
✅ Successfully connected to Backend-Socket server
📨 Status: Printer client connected and joined room
```

**Print Requests:**
```
🖨️ Print request received
   Type: receipt
   Printer: RONGTA 80mm Series Printer
✅ Print job completed successfully
```

**Errors:**
```
❌ Connection failed: Connection refused
❌ Print job failed
```

### Color Coding
- 🔵 **Blue** = Information (normal operations)
- 🟡 **Yellow** = Warnings
- 🔴 **Red** = Errors

## 🖨️ Supported Printers

Works with any Windows printer:
- Thermal receipt printers (like RONGTA 80mm)
- Standard office printers
- PDF printers
- Network printers

Your available printers appear in the dropdown menu.

## 🧪 Testing

### Test Print Button
1. Connect to server
2. Click **🖨️ Test Print**
3. Check your printer for output

The test print includes:
- Test message
- Current date/time
- Printer name
- Connection status

## 📊 Statistics

Bottom of the Activity Log shows:
- **Prints:** Total successful print jobs
- **Errors:** Total errors encountered

Statistics help you monitor system health.

## 🔒 Connection Status

### Indicators

**🔴 Red Circle + "Disconnected"**
- Not connected to server
- Test Print button disabled
- Connect button available

**🟢 Green Circle + "Connected"**
- Active connection to Backend-Socket
- Test Print button enabled
- Shows Client ID
- Disconnect button available

## 💾 Saving Configuration

When you change settings:
1. Update the values
2. Click **💾 Save Configuration**
3. Settings saved to `.env` file
4. Confirmation message appears

Configuration persists when you restart the app.

## 🚪 Closing the App

When you close the window:
- If connected, asks "Do you want to quit?"
- Automatically disconnects from server
- Saves current state
- Closes cleanly

## 🆚 GUI vs Console

| Feature | GUI App | Console App |
|---------|---------|-------------|
| **Interface** | Visual window | Text only |
| **Configuration** | Click & type | Edit .env file |
| **Logs** | Colored, scrollable | Plain text |
| **Connection Status** | Visual indicator | Text messages |
| **NIPT Change** | Type & save | Edit file & restart |
| **Test Print** | One button | Write script |
| **User Friendly** | ⭐⭐⭐⭐⭐ | ⭐⭐ |

**Recommendation:** Use the GUI app! It's much easier.

## 🔄 Auto-Start on Windows Boot

### Option 1: Startup Folder
1. Press `Win+R`, type `shell:startup`, press Enter
2. Create shortcut to `start_gui.bat`
3. Application starts when Windows starts

### Option 2: Task Scheduler
1. Open Task Scheduler
2. Create new task
3. Trigger: At log on
4. Action: Start `start_gui.bat`
5. Application runs in background

## 🐛 Troubleshooting

### GUI doesn't open
- Right-click `start_gui.bat`, choose "Run as administrator"
- Check if Python is installed
- Verify virtual environment exists in `venv` folder

### Can't connect to server
- Check Activity Log for error details
- Verify Backend-Socket is running: http://127.0.0.1:5001
- Check NIPT value matches server expectations
- Verify firewall isn't blocking connection

### Printer doesn't work
- Click **🖨️ Test Print** to verify
- Check printer is turned on
- Verify printer in Windows settings
- Select different printer from dropdown

### Activity Log shows errors
- Red text = errors (read the message)
- Common: "Connection refused" = server not running
- Common: "Print failed" = printer not ready

## 📁 Files

| File | Purpose |
|------|---------|
| `printer_client_gui.py` | Main GUI application |
| `start_gui.bat` | Quick start script |
| `printer_client_gui.log` | Application log file |
| `.env` | Configuration (editable in GUI) |

## 💡 Tips & Tricks

1. **Pin to Taskbar**: Right-click `start_gui.bat` → Send to → Desktop, then pin the shortcut
2. **Always On Top**: Resize window small, keep visible while working
3. **Monitor Logs**: Watch Activity Log to see requests come in
4. **Save Often**: Click Save Configuration after any changes
5. **Test Regularly**: Use Test Print to verify printer connection

## 🎯 Common Use Cases

### Restaurant POS
- Set NIPT to restaurant identifier
- Connect to Backend-Socket
- Receipts print automatically when orders complete

### Reservation System
- Configure reservation printer
- Confirmation tickets print automatically
- Monitor activity in real-time

### Multi-Location Setup
- Each location has one printer client
- Unique NIPT per location
- Central Backend-Socket server

## 🚀 Next Steps

1. **Start the app:** Double-click `start_gui.bat`
2. **Configure NIPT:** Enter your company NIPT value
3. **Connect:** Click the Connect button
4. **Test:** Click Test Print
5. **Monitor:** Watch the Activity Log

You're ready to go!

## 📚 Additional Documentation

- **Full Documentation:** README.md
- **GUI Guide:** GUI_GUIDE.md
- **Integration:** INTEGRATION_GUIDE.md
- **Quick Start:** QUICKSTART.md

## 🆘 Support

If you encounter issues:
1. Check Activity Log for error messages
2. Review this documentation
3. Check Backend-Socket is running
4. Verify NIPT configuration
5. Test printer with Test Print button

---

**Enjoy your visual printer management experience!** 🎉
