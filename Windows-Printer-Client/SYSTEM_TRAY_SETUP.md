# Print Client Pro - System Tray Setup

## Overview
Print Client Pro can run as a background service in your Windows system tray, automatically starting when Windows boots.

## Features
- **System Tray Icon**: Shows printer icon in system tray (bottom-right corner)
- **Auto-Start**: Runs automatically when Windows starts
- **Background Service**: Works silently in background
- **Quick Access**: Click tray icon to show/hide the GUI
- **Always Running**: Handles print requests even when window is hidden

## Installation Steps

### 1. Install as Startup Service

**Double-click**: `install_startup.bat`

This will:
- Create a shortcut in Windows Startup folder
- Configure the app to start automatically on boot
- Hide the console window (runs silently)

### 2. Start the Service Now

**Double-click**: `run_tray.bat`

This will:
- Start Print Client Pro in system tray
- Show a printer icon in your system tray (bottom-right)

### 3. Using the System Tray

**Look for**: Printer icon in system tray (🖨️)

**Right-click the icon** to see menu:
- **Print Client Pro** - Open the GUI window
- **Show Window** - Show the GUI window
- **Hide Window** - Hide the GUI window
- **Exit** - Close the application completely

**Left-click the icon** (or double-click) to open the GUI window

### 4. Remove from Startup (Optional)

**Double-click**: `remove_startup.bat`

This will:
- Remove the app from Windows Startup
- Stop auto-starting on boot
- (Note: Won't stop current running instance)

## How It Works

### Background Operation
- The app runs in the background using `printer_client_tray.py`
- Listens for print requests from Backend-Socket 24/7
- No console window visible
- Minimal system resources

### GUI Window
- **Hidden by default** when running as service
- **Click tray icon** to show the window
- **Close button** hides the window (doesn't exit)
- **Exit from tray menu** to fully quit

### Auto-Start Behavior
- After installation, the app starts automatically when:
  - Windows boots/restarts
  - User logs in
  - PC wakes from sleep
- No manual intervention needed

## Files Created

After installation:
- `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PrintClientPro.lnk`
- `run_hidden.vbs` (in this folder)

## Manual Start Options

### Option 1: System Tray (Recommended)
```
run_tray.bat
```
- Runs in background with tray icon
- Best for production use

### Option 2: Direct GUI (For Testing)
```
venv\Scripts\python.exe printer_client_gui.py
```
- Opens GUI directly
- Shows console window
- Good for debugging

## Troubleshooting

### Tray Icon Not Showing?
1. Check if app is running (Task Manager → Details → pythonw.exe)
2. Click the arrow (^) in system tray to show hidden icons
3. Right-click system tray → Taskbar settings → Select which icons appear

### App Not Starting on Boot?
1. Run `install_startup.bat` again
2. Check Windows Startup apps: Settings → Apps → Startup
3. Look for "PrintClientPro" shortcut

### Can't See the GUI Window?
1. Right-click tray icon
2. Click "Show Window"
3. If still hidden, click "Exit" and run `run_tray.bat` again

### Want to Stop the App?
1. Right-click tray icon
2. Click "Exit"
3. Or kill from Task Manager (pythonw.exe)

## Command Line Options

### Start in Background
```batch
venv\Scripts\pythonw.exe printer_client_tray.py
```

### Start with Console (Debug)
```batch
venv\Scripts\python.exe printer_client_tray.py
```

## Security Notes

- The app runs under your user account
- No admin privileges required
- All settings saved in local folder
- Connection uses WebSocket (check firewall if issues)

## Support

If you encounter issues:
1. Check `printer_client_gui.log` for errors
2. Run from console to see error messages
3. Ensure all dependencies installed: `pip install -r requirements.txt`
