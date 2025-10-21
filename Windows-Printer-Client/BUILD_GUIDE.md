# Print Client Pro - Build and Distribution Guide

Complete guide for building and distributing Print Client Pro to client PCs.

## Overview

This guide covers:
1. Building the executable with PyInstaller
2. Creating the Windows installer with Inno Setup
3. Distributing to client computers
4. Preparing for Windows Store submission

## Prerequisites

### Required Software
1. **Python 3.11+** (already installed in venv)
2. **PyInstaller** (already installed)
3. **Inno Setup 6** - Download from: https://jrsoftware.org/isdl.php

### Optional (for Windows Store)
4. **Visual Studio** - For UWP packaging
5. **Windows SDK** - For app certification

## Step 1: Build the Executable

### Option A: Using the Build Script (Recommended)
```cmd
build.bat
```

This will:
- Clean previous builds
- Run PyInstaller with the spec file
- Create `dist\PrintClientPro.exe`

### Option B: Manual Build
```cmd
venv\Scripts\pyinstaller.exe --clean --noconfirm PrintClientPro.spec
```

### Build Output
After successful build:
- **Executable**: `dist\PrintClientPro.exe`
- **Size**: ~50-80 MB (includes Python runtime and dependencies)
- **Type**: Single-file executable (no installation required for testing)

### Testing the Executable
```cmd
cd dist
PrintClientPro.exe
```

The app should:
1. Start in system tray
2. Show printer icon (may be in hidden icons)
3. Click icon to open GUI

## Step 2: Create the Windows Installer

### Install Inno Setup
1. Download from: https://jrsoftware.org/isdl.php
2. Install with default options
3. Note the installation path (usually `C:\Program Files (x86)\Inno Setup 6`)

### Build the Installer

#### Option A: Using Inno Setup Compiler GUI
1. Open Inno Setup Compiler
2. Open `installer.iss`
3. Click **Build > Compile**
4. Wait for completion

#### Option B: Using Command Line
```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Installer Output
After successful compilation:
- **Location**: `installer_output\PrintClientPro_Setup_v1.0.0.exe`
- **Size**: ~50-80 MB
- **Features**:
  - Professional Windows installer
  - Configuration wizard during installation
  - Auto-start option
  - Desktop shortcut option
  - Uninstaller included

## Step 3: Test the Installer

### Testing Process
1. Run `installer_output\PrintClientPro_Setup_v1.0.0.exe`
2. Follow installation wizard
3. Enter test configuration:
   - Server URL: `http://127.0.0.1:5001`
   - NIPT: Your company ID
   - Username: Test user
   - Session ID: Test session
4. Choose auto-start option
5. Complete installation
6. Verify app starts in system tray

### Verify Installation
Check these locations:
- **Installation**: `C:\Program Files\Print Client Pro\`
- **Executable**: `C:\Program Files\Print Client Pro\PrintClientPro.exe`
- **Config**: `C:\Program Files\Print Client Pro\.env`
- **Startup**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Print Client Pro.lnk` (if selected)

### Test Uninstallation
1. Right-click tray icon > Exit
2. Windows Settings > Apps > Print Client Pro > Uninstall
3. Verify all files removed

## Step 4: Distribution to Clients

### Distribution Methods

#### Method 1: Direct Download (Recommended for Testing)
1. Host `PrintClientPro_Setup_v1.0.0.exe` on your server
2. Provide download link to clients
3. Clients download and run installer
4. Follow installation wizard

#### Method 2: USB/Network Share
1. Copy `PrintClientPro_Setup_v1.0.0.exe` to USB or network share
2. Clients run installer from USB/network
3. Follow installation wizard

#### Method 3: Remote Deployment (IT Managed)
Use enterprise deployment tools:
- **Group Policy**: Deploy via GPO
- **SCCM**: System Center Configuration Manager
- **Intune**: Microsoft Intune deployment
- **PDQ Deploy**: For small businesses

### Silent Installation (IT Deployment)
For automated deployment without user interaction:

```cmd
PrintClientPro_Setup_v1.0.0.exe /VERYSILENT /NORESTART /TASKS="startupicon"
```

Parameters:
- `/VERYSILENT` - No UI, no prompts
- `/NORESTART` - Don't restart computer
- `/TASKS="startupicon"` - Enable auto-start
- `/DIR="C:\Custom\Path"` - Custom install location

### Pre-configured Installation
Create a config file for automated setup:

1. Create `setup_config.inf`:
```ini
[Setup]
ServerURL=http://your-server.com:5001
NIPT=YOUR_COMPANY_ID
Username=DefaultUser
SessionID=DefaultSession
```

2. Modify `installer.iss` to read from config file
3. Rebuild installer

## Step 5: Client Setup Instructions

Provide these instructions to clients:

### Installation Steps
1. Download `PrintClientPro_Setup_v1.0.0.exe`
2. Right-click > Run as Administrator (if needed)
3. Click **Next** through welcome screens
4. Accept license agreement
5. Choose installation location (default recommended)
6. **Important**: Enter your configuration:
   - **Server URL**: `http://[YOUR_SERVER_IP]:5001`
   - **NIPT**: Your company ID (provided by IT)
   - **Username**: Your username
   - **Session ID**: Your session ID (optional)
7. Check "Start automatically with Windows" (recommended)
8. Uncheck "Create desktop icon" (optional, runs in tray anyway)
9. Click **Install**
10. Click **Finish** (app starts automatically)

### First Use
1. Look for printer icon in system tray (bottom-right)
2. If not visible, click the arrow (^) to show hidden icons
3. Right-click icon > Show Window to open GUI
4. Click **Connect** button
5. Verify connection status shows "Connected"
6. Run a test print (if needed)

### Daily Use
- App runs automatically in background
- No user interaction needed
- Print jobs processed automatically
- Check system tray icon for status

## Step 6: Windows Store Preparation

For future Windows Store submission:

### Requirements
1. **Microsoft Developer Account** ($19 one-time fee)
2. **App Certification** - Must pass Windows App Certification Kit
3. **Privacy Policy** - Required for store apps
4. **Screenshots** - At least 1, recommended 4-5
5. **App Icon** - Multiple sizes (already have printer_icon.ico)

### Conversion to UWP (Future)
To publish on Windows Store, you'll need to:

1. **Create UWP Package**:
   ```cmd
   # Install Desktop Bridge
   # Convert Win32 app to UWP
   MakeAppx.exe pack /d dist /p PrintClientPro.msix
   ```

2. **Sign the Package**:
   ```cmd
   SignTool.exe sign /fd SHA256 /a /f MyCert.pfx PrintClientPro.msix
   ```

3. **Test on Windows**:
   - Install the MSIX package
   - Verify all functionality works
   - Run App Certification Kit

4. **Submit to Store**:
   - Go to Partner Center
   - Create new app submission
   - Upload MSIX package
   - Fill in app details
   - Submit for certification

### Alternative: Microsoft Store for Business
- Deploy privately to your organization
- No public store listing needed
- Easier certification process

## Build Files Summary

### Essential Build Files
```
Windows-Printer-Client/
├── PrintClientPro.spec          # PyInstaller build configuration
├── version_info.txt             # Windows version information
├── printer_icon.ico             # Application icon
├── installer.iss                # Inno Setup installer script
├── LICENSE.txt                  # Software license
├── README.md                    # User documentation
└── BUILD_GUIDE.md              # This file

Build Scripts:
├── build.bat                    # Build executable
└── create_icon.py              # Generate icon

Source Files:
├── printer_client_tray.py      # System tray wrapper (entry point)
├── printer_client_gui.py       # Main GUI application
├── printer_handler.py          # Printer operations
└── requirements.txt            # Python dependencies

Output:
├── dist/                        # PyInstaller output
│   └── PrintClientPro.exe      # Standalone executable
└── installer_output/           # Inno Setup output
    └── PrintClientPro_Setup_v1.0.0.exe  # Windows installer
```

### File Sizes (Approximate)
- `PrintClientPro.exe`: 50-80 MB
- `PrintClientPro_Setup_v1.0.0.exe`: 50-80 MB (includes exe + installer logic)
- Total distribution size: ~80 MB

## Troubleshooting Build Issues

### PyInstaller Errors

**Missing Modules**:
```
Add to PrintClientPro.spec hiddenimports:
hiddenimports=['module_name']
```

**Import Errors**:
```
Update requirements.txt and rebuild
```

**Large File Size**:
```
Exclude unnecessary packages in spec file:
excludes=['matplotlib', 'pandas', 'numpy']
```

### Inno Setup Errors

**File Not Found**:
- Verify `dist\PrintClientPro.exe` exists
- Run build.bat first

**Icon Not Found**:
- Verify `printer_icon.ico` exists
- Run `python create_icon.py` if missing

**Version Mismatch**:
- Update version in `installer.iss` and `version_info.txt`

## Version Updates

When releasing new versions:

1. **Update Version Numbers**:
   - `version_info.txt`: Update FileVersion and ProductVersion
   - `installer.iss`: Update #define MyAppVersion
   - `README.md`: Add to Version History

2. **Rebuild Everything**:
   ```cmd
   build.bat
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

3. **Test New Installer**:
   - Install on clean system
   - Verify upgrade from previous version
   - Test all features

4. **Distribute**:
   - Upload new installer
   - Notify clients of update
   - Provide changelog

## Security Considerations

### Code Signing (Highly Recommended)
For production distribution:

1. **Get Code Signing Certificate**:
   - Purchase from DigiCert, Sectigo, or other CA
   - Cost: ~$200-400/year
   - Verifies publisher identity

2. **Sign the Executable**:
   ```cmd
   signtool.exe sign /f MyCert.pfx /p PASSWORD /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 dist\PrintClientPro.exe
   ```

3. **Sign the Installer**:
   - Add to `installer.iss`:
   ```
   SignTool=signtool.exe sign /f MyCert.pfx /p PASSWORD /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 $f
   SignedUninstaller=yes
   ```

### Benefits of Code Signing
- No Windows SmartScreen warnings
- Users trust the installer
- Required for Windows Store
- Professional appearance

## Support and Maintenance

### Client Support
Provide clients with:
1. README.md (user guide)
2. Support contact information
3. Troubleshooting steps
4. Update notification method

### Update Strategy
1. **Auto-update** (future enhancement):
   - Check for updates on startup
   - Download and install automatically
   - Or notify user of available update

2. **Manual update**:
   - Download new installer
   - Run installer (upgrades existing installation)
   - Configuration preserved

### Logging and Diagnostics
Logs stored in installation directory:
- `printer_client_gui.log` - Application logs
- Help clients send logs for troubleshooting

## Conclusion

You now have a complete, professional distribution package for Print Client Pro:

✅ Standalone executable (PyInstaller)
✅ Professional Windows installer (Inno Setup)
✅ Auto-start configuration
✅ First-time setup wizard
✅ System tray background service
✅ Comprehensive documentation
✅ Ready for client distribution
✅ Prepared for future Windows Store submission

### Next Steps
1. Build the executable: `build.bat`
2. Create the installer: Compile `installer.iss`
3. Test installation on a clean system
4. Distribute to clients
5. (Optional) Submit to Windows Store

For questions or issues, refer to the specific sections above.
