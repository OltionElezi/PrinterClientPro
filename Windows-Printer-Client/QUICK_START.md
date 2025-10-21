# Print Client Pro - Quick Start Guide

Fast setup guide for building and distributing your printer client.

## 🚀 Quick Build (5 Minutes)

### Step 1: Build the Executable
```cmd
cd C:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
build.bat
```

Wait for completion. Output: `dist\PrintClientPro.exe`

### Step 2: Test the Executable
```cmd
cd dist
PrintClientPro.exe
```

Look for printer icon in system tray. Click to open GUI.

## 📦 Create Installer (If you have Inno Setup)

### Option 1: You Have Inno Setup Installed
```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

Output: `installer_output\PrintClientPro_Setup_v1.0.0.exe`

### Option 2: Don't Have Inno Setup
1. Download from: https://jrsoftware.org/isdl.php
2. Install it
3. Open `installer.iss` in Inno Setup
4. Click Build > Compile

## 📤 Distribute to Clients

### Simple Distribution (Just the EXE)
Share `dist\PrintClientPro.exe` with clients:
- Copy to USB drive
- Email (if size allows)
- Upload to file sharing
- Network share

Clients just double-click to run!

### Professional Distribution (Installer)
Share `PrintClientPro_Setup_v1.0.0.exe`:
- Professional installation wizard
- Automatic configuration setup
- Auto-start on Windows boot
- Proper uninstaller

## ⚙️ Client Configuration

### If Using Just the EXE
Clients need to create `.env` file next to `PrintClientPro.exe`:

```env
SOCKET_SERVER_URL=http://YOUR_SERVER:5001
NIPT=COMPANY_ID
USERNAME=user
SESSION_ID=session
RECONNECT_DELAY=5
MAX_RECONNECT_ATTEMPTS=0
```

### If Using the Installer
Configuration is done during installation via wizard. No manual setup needed!

## 🎯 What Clients Need to Know

### Installation
1. Run the installer (or EXE)
2. Enter server connection details
3. App starts in system tray
4. Look for printer icon near clock

### Daily Use
- App runs automatically in background
- Minimizing window hides it to tray (keeps running)
- Right-click tray icon to exit completely
- Print jobs processed automatically

### Troubleshooting
- **Can't see tray icon**: Click arrow (^) near clock
- **Connection failed**: Check server URL in configuration
- **Print not working**: Verify printer is installed

## 📋 Files You Need

### For Building
- ✅ All files already created
- ✅ `build.bat` - Run this to build
- ✅ `PrintClientPro.spec` - Build configuration
- ✅ `printer_icon.ico` - App icon

### For Installer
- ✅ `installer.iss` - Installer script
- ✅ `LICENSE.txt` - License agreement
- ✅ `README.md` - User documentation

### For Distribution
Choose one:
- `dist\PrintClientPro.exe` (standalone)
- `PrintClientPro_Setup_v1.0.0.exe` (installer)

## 🔥 Common Commands

### Rebuild Everything
```cmd
build.bat
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Clean Build
```cmd
rmdir /s /q build dist
build.bat
```

### Test Locally
```cmd
dist\PrintClientPro.exe
```

## 💡 Pro Tips

### For Multiple Clients
Create different installers with pre-configured settings:
1. Modify `installer.iss` default values
2. Set server URL, NIPT, etc.
3. Build custom installer per client
4. Clients get instant setup!

### Background Service
The app already:
- ✅ Runs in system tray
- ✅ Starts with Windows (if installed with installer)
- ✅ Continues running when window closed
- ✅ Reconnects automatically to server
- ✅ Processes prints in background

No additional setup needed!

### Windows Store (Future)
For Windows Store submission:
- See full BUILD_GUIDE.md
- Requires UWP conversion
- Need Microsoft Developer account ($19)
- Additional certification steps

## 📞 Need Help?

- **Build issues**: Check BUILD_GUIDE.md
- **Distribution**: See BUILD_GUIDE.md Step 4
- **Windows Store**: See BUILD_GUIDE.md Step 6

## ✨ You're Ready!

You now have everything needed to distribute Print Client Pro to any number of clients!

**Current Status:**
- ✅ Executable built with PyInstaller
- ✅ Installer ready with Inno Setup
- ✅ Auto-start configured
- ✅ Background service working
- ✅ Professional distribution package

**Just run:**
```cmd
build.bat
```

Then share the installer with clients. Done! 🎉
