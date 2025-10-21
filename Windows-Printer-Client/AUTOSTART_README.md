# PrintClientPro - Auto-Start Setup Guide

This guide will help you configure PrintClientPro to start automatically when Windows boots.

## 📦 Files Included

- `setup_autostart.bat` - Sets up automatic startup
- `remove_autostart.bat` - Removes automatic startup
- `PrintClientPro.exe` - The main executable (in `dist/` folder)

## ✅ Setup Instructions

### Method 1: Using the Setup Script (RECOMMENDED)

1. **Navigate to the folder:**
   ```
   C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client
   ```

2. **Double-click `setup_autostart.bat`**
   - This will create a shortcut in your Windows Startup folder
   - No administrator rights needed
   - The app will start automatically when you log into Windows

3. **Verify Setup:**
   - Check your Startup folder by pressing `Win + R` and typing: `shell:startup`
   - You should see `PrintClientPro.lnk` shortcut there

### Method 2: Manual Setup

1. **Open Windows Startup folder:**
   - Press `Win + R`
   - Type: `shell:startup`
   - Press Enter

2. **Create a shortcut:**
   - Right-click in the Startup folder
   - Select "New" → "Shortcut"
   - Browse to: `C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client\dist\PrintClientPro.exe`
   - Name it "PrintClientPro"
   - Click Finish

### Method 3: Task Scheduler (Advanced - Runs Before Login)

If you need the app to start before you log in (system-level):

1. Open Task Scheduler (search in Start menu)
2. Click "Create Task" (not "Create Basic Task")
3. **General Tab:**
   - Name: `PrintClientPro AutoStart`
   - Description: `Starts PrintClientPro automatically`
   - Select "Run whether user is logged on or not"
   - Check "Run with highest privileges"

4. **Triggers Tab:**
   - Click "New"
   - Begin the task: "At startup"
   - Click OK

5. **Actions Tab:**
   - Click "New"
   - Action: "Start a program"
   - Program/script: `C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client\dist\PrintClientPro.exe`
   - Start in: `C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client\dist`
   - Click OK

6. **Conditions Tab:**
   - Uncheck "Start the task only if the computer is on AC power"

7. **Settings Tab:**
   - Check "Allow task to be run on demand"
   - Check "Run task as soon as possible after a scheduled start is missed"

8. Click OK and save

## 🛑 Remove Auto-Start

### Option 1: Using the Remove Script
- Double-click `remove_autostart.bat`

### Option 2: Manual Removal
1. Press `Win + R`
2. Type: `shell:startup`
3. Delete the `PrintClientPro.lnk` shortcut

### Option 3: Task Scheduler Removal
1. Open Task Scheduler
2. Find "PrintClientPro AutoStart" in the task list
3. Right-click and select "Delete"

## 🔍 Verify Auto-Start is Working

1. **Restart your computer**
2. **After Windows boots and you log in:**
   - PrintClientPro should automatically start
   - Check the system tray for the application icon
   - The GUI window should appear

## 📝 Important Notes

- **Location matters:** If you move the `dist` folder or the executable, you'll need to reconfigure auto-start
- **User-level startup:** Method 1 and 2 start the app when YOU log in
- **System-level startup:** Method 3 can start the app at system boot (before login)
- **Dependencies:** Make sure all required files stay in the `dist` folder:
  - `PrintClientPro.exe`
  - `.env` file (configuration)
  - `SumatraPDF.exe`
  - `wkhtmltopdf.exe`
  - Any other DLL or support files

## 🔧 Troubleshooting

### App doesn't start automatically:
1. Check if the shortcut exists in the Startup folder
2. Verify the exe path in the shortcut is correct
3. Check Windows Event Viewer for errors

### App starts but doesn't connect:
1. Make sure `.env` file is in the `dist` folder
2. Verify your configuration settings
3. Check network connectivity

### Multiple instances starting:
1. Check if you have multiple shortcuts in Startup folder
2. Check Task Scheduler for duplicate tasks
3. Remove duplicates and keep only one

## 📍 File Locations

- **Executable:** `C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client\dist\PrintClientPro.exe`
- **Startup Folder:** `C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
- **Config File:** `C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client\dist\.env`

## ✨ Testing

To test without restarting:
1. Open the Startup folder: `Win + R` → `shell:startup`
2. Double-click the `PrintClientPro` shortcut
3. The app should start normally

---

**Need Help?** If you encounter any issues, check the log file at:
`C:\Users\user\Desktop\ParidBackend\PrinterClientPro\Windows-Printer-Client\dist\printer_client_gui.log`
