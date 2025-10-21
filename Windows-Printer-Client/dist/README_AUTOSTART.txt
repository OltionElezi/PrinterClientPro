================================================
   PrintClientPro - Auto-Start Configuration
================================================

QUICK START GUIDE
=================

1. SETUP AUTO-START (First Time)
   ------------------------------
   Double-click: SETUP_AUTOSTART.bat

   This will:
   - Configure Windows to start PrintClientPro on boot
   - Create/verify .env configuration file
   - Set up all necessary shortcuts

2. REMOVE AUTO-START (If Needed)
   ------------------------------
   Double-click: REMOVE_AUTOSTART.bat

   This will:
   - Remove auto-start configuration
   - Keep all program files intact


WHAT FILES ARE IN THIS FOLDER?
===============================

Core Application:
  - PrintClientPro.exe          Main application
  - .env                        Configuration file

Auto-Start Scripts:
  - SETUP_AUTOSTART.bat         Setup wizard
  - REMOVE_AUTOSTART.bat        Remove auto-start
  - README_AUTOSTART.txt        This file

PDF Converters:
  - wkhtmltopdf.exe            Primary PDF converter (recommended)
  - SumatraPDF.exe             Alternative PDF viewer/converter

Data Files:
  - printer_settings.json       Your printer configurations
  - printer_client_gui.log      Application log file


HOW AUTO-START WORKS
====================

When you run SETUP_AUTOSTART.bat, it creates a shortcut here:
  C:\Users\[YOUR_USERNAME]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

This shortcut points to:
  [THIS_FOLDER]\PrintClientPro.exe

Windows automatically runs all shortcuts in the Startup folder
when you log into your PC.


CONFIGURATION (.env file)
=========================

The .env file contains your settings:
  - SOCKET_URL          Server address
  - NIPT                Company ID
  - SESSION_ID          Session identifier
  - CLIENT_USERNAME     Client username
  - PDF_CONVERTER       PDF conversion method

You can edit this file in two ways:
  1. Use the GUI (recommended):
     - Start PrintClientPro.exe
     - Click "Configuration" button
     - Edit settings
     - Click "Save"

  2. Edit .env file directly:
     - Open .env with Notepad
     - Change values
     - Save file
     - Restart PrintClientPro


TESTING AUTO-START
==================

Method 1: Without Restarting PC
  1. Press Windows Key + R
  2. Type: shell:startup
  3. Press Enter
  4. Double-click "PrintClientPro" shortcut

Method 2: Full Test
  1. Restart your computer
  2. Log into Windows
  3. PrintClientPro should start automatically


MOVING THE APPLICATION
======================

IMPORTANT: If you move this folder to a different location:
  1. Run REMOVE_AUTOSTART.bat (in the OLD location)
  2. Move the entire folder to the new location
  3. Run SETUP_AUTOSTART.bat (in the NEW location)

The auto-start shortcut contains the full path to PrintClientPro.exe,
so it must be updated if you move the folder.


TROUBLESHOOTING
===============

Problem: Auto-start doesn't work after PC restart
  Solution 1: Run SETUP_AUTOSTART.bat again
  Solution 2: Check Windows Startup folder (Win+R → shell:startup)
  Solution 3: Check if Windows blocks the shortcut

Problem: Application starts but doesn't connect
  Solution 1: Check .env file configuration
  Solution 2: Verify SOCKET_URL is correct
  Solution 3: Check network connection
  Solution 4: Review printer_client_gui.log for errors

Problem: Setup script fails
  Solution: Run SETUP_AUTOSTART.bat as Administrator
            (Right-click → Run as Administrator)

Problem: Multiple instances starting
  Solution 1: Check Startup folder for duplicate shortcuts
  Solution 2: Run REMOVE_AUTOSTART.bat
  Solution 3: Run SETUP_AUTOSTART.bat again


PORTABLE INSTALLATION
=====================

This application is fully portable! You can:
  1. Copy this entire folder to a USB drive
  2. Move it to another PC
  3. Run SETUP_AUTOSTART.bat on the new PC
  4. Everything works with the same configuration

Requirements on new PC:
  - Windows 7 or later
  - No administrator rights needed (for auto-start)


UNINSTALL
=========

Complete Removal:
  1. Run REMOVE_AUTOSTART.bat
  2. Close PrintClientPro if running
  3. Delete this entire folder

The application doesn't install anything outside this folder
(except the shortcut in the Startup folder, which is removed
by REMOVE_AUTOSTART.bat)


SECURITY NOTES
==============

- Your configuration (NIPT, credentials) is stored in .env file
- This file is NOT encrypted
- Keep this folder secure
- Don't share .env file with unauthorized users
- The auto-start shortcut only runs YOUR exe file
- No system files are modified


FILE LOCATIONS
==============

This Folder:
  %CURRENT_FOLDER%

Startup Shortcut:
  %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PrintClientPro.lnk

Quick way to open Startup folder:
  Press: Windows Key + R
  Type: shell:startup
  Press: Enter


SUPPORT
=======

For issues or questions:
  1. Check printer_client_gui.log for errors
  2. Verify .env configuration
  3. Test with VERIFY_FILES.bat
  4. Contact your system administrator


VERSION INFORMATION
===================

Application: PrintClientPro
Type: Windows Printer Client
Auto-Start: Windows Startup Folder Method


================================================
           End of Documentation
================================================
