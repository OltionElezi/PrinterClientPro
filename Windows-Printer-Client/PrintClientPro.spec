# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Print Client Pro
Creates a standalone Windows executable with all dependencies
"""

import os
import shutil

block_cipher = None

# Collect data files
datas = []
if os.path.exists('printer_icon.ico'):
    datas.append(('printer_icon.ico', '.'))

# Collect binaries (wkhtmltopdf for PDF conversion)
# Note: We DON'T bundle wkhtmltopdf in binaries because it's large and may have DLL dependencies
# Instead, we copy it to dist folder after build
binaries = []

# Check for wkhtmltopdf executable - we'll copy it separately
wkhtmltopdf_paths = [
    r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
    r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
]

wkhtmltopdf_source = None
for wkhtml_path in wkhtmltopdf_paths:
    if os.path.exists(wkhtml_path):
        print(f"Found wkhtmltopdf at: {wkhtml_path}")
        wkhtmltopdf_source = wkhtml_path
        print("wkhtmltopdf.exe will be copied to dist folder after build")
        break

if not wkhtmltopdf_source:
    print("WARNING: wkhtmltopdf.exe not found - PDF printing may not work on target machine!")
    print("Install from: https://wkhtmltopdf.org/downloads.html")

# Check for SumatraPDF executable
sumatrapdf_paths = [
    r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
    r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
    os.path.join(SPECPATH, "dist", "SumatraPDF.exe"),
    os.path.join(SPECPATH, "SumatraPDF.exe"),
]

sumatrapdf_source = None
for sumatra_path in sumatrapdf_paths:
    if os.path.exists(sumatra_path):
        print(f"Found SumatraPDF at: {sumatra_path}")
        sumatrapdf_source = sumatra_path
        print("SumatraPDF.exe will be copied to dist folder after build")
        break

if not sumatrapdf_source:
    print("WARNING: SumatraPDF.exe not found - will use fallback printing method")
    print("Download from: https://www.sumatrapdfreader.org/download-free-pdf-viewer")

a = Analysis(
    ['printer_client_tray.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'socketio',
        'engineio',
        'win32print',
        'win32ui',
        'win32con',
        'win32api',
        'pywintypes',
        'PIL',
        'PIL._tkinter_finder',
        'pystray',
        'bs4',
        'dotenv',
        'pdfkit',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib.units',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'qrcode',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PrintClientPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window - runs in background
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='printer_icon.ico' if os.path.exists('printer_icon.ico') else None,
    version_file='version_info.txt' if os.path.exists('version_info.txt') else None,
)

# Post-build: Copy wkhtmltopdf.exe and SumatraPDF.exe to dist folder
dist_dir = os.path.join(SPECPATH, 'dist')

if os.path.exists(dist_dir):
    # Copy wkhtmltopdf.exe
    if wkhtmltopdf_source and os.path.exists(wkhtmltopdf_source):
        wkhtmltopdf_dest = os.path.join(dist_dir, 'wkhtmltopdf.exe')
        try:
            shutil.copy2(wkhtmltopdf_source, wkhtmltopdf_dest)
            print(f"\nCopied wkhtmltopdf.exe to dist folder")
            print(f"   Source: {wkhtmltopdf_source}")
            print(f"   Dest: {wkhtmltopdf_dest}")
        except Exception as e:
            print(f"\nWARNING: Failed to copy wkhtmltopdf.exe: {e}")

    # Copy SumatraPDF.exe
    if sumatrapdf_source and os.path.exists(sumatrapdf_source):
        sumatrapdf_dest = os.path.join(dist_dir, 'SumatraPDF.exe')
        try:
            shutil.copy2(sumatrapdf_source, sumatrapdf_dest)
            print(f"\nCopied SumatraPDF.exe to dist folder")
            print(f"   Source: {sumatrapdf_source}")
            print(f"   Dest: {sumatrapdf_dest}")
        except Exception as e:
            print(f"\nWARNING: Failed to copy SumatraPDF.exe: {e}")
else:
    print(f"\nWARNING: dist folder not found yet, external executables will not be copied")
