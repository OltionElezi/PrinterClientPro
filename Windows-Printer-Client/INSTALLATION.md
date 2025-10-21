# Installation Guide - HTML Printing Support

## Overview

This guide will help you set up the new HTML to PDF printing functionality in the Windows Printer Client.

## Prerequisites

- Windows 10 or later
- Python 3.8 or higher
- Existing Windows Printer Client installation

## Installation Steps

### Step 1: Update Dependencies

Navigate to your Windows-Printer-Client directory and install the new dependencies:

```bash
cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
pip install -r requirements.txt
```

This will install:
- `weasyprint` - Primary HTML to PDF converter
- `reportlab` - Fallback PDF generator
- Other required dependencies

### Step 2: Verify Installation

Check that the packages are installed:

```bash
pip list | findstr weasyprint
pip list | findstr reportlab
```

You should see:
```
weasyprint    60.x.x
reportlab     4.x.x
```

### Step 3: Install SumatraPDF (Optional but Recommended)

For best printing results on Windows:

1. Download SumatraPDF from: https://www.sumatrapdfreader.org/download-free-pdf-viewer
2. Run the installer
3. Install to the default location: `C:\Program Files\SumatraPDF\`

**Why SumatraPDF?**
- Silent printing (no print dialogs)
- Better thermal printer support
- Faster and more reliable
- Lightweight (only ~5MB)

### Step 4: Restart the Client

Restart the Windows Printer Client service:

1. Right-click the system tray icon
2. Select "Exit"
3. Start the client again (or it will auto-start if configured)

### Step 5: Test HTML Printing

Send a test print request with HTML content:

```json
{
  "printer_name": "Your Printer Name",
  "content": "<!DOCTYPE html><html><head><style>body{text-align:center;}</style></head><body><h1>Test Print</h1><p>HTML printing is working!</p></body></html>"
}
```

Check the logs for:
```
[INFO] Auto-detected HTML content
[INFO] Converting HTML to PDF...
[INFO] HTML converted to PDF: ...
[INFO] Printing PDF to ...
[INFO] HTML printed successfully via PDF conversion
```

## Troubleshooting Installation

### WeasyPrint Installation Fails

**Error**: "Failed building wheel for weasyprint"

**Solution**:
1. Install GTK+ for Windows:
   - Download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
   - Run the installer
   - Restart your computer

2. Try installing again:
   ```bash
   pip install weasyprint
   ```

### Alternative: Use ReportLab Only

If WeasyPrint installation fails, the system will automatically fall back to ReportLab (which is easier to install):

```bash
pip install reportlab beautifulsoup4
```

Note: ReportLab provides basic HTML to PDF conversion. WeasyPrint offers better CSS support and rendering quality.

### Missing Dependencies

If you see errors about missing modules:

```bash
pip install python-socketio[client]==5.10.0 python-dotenv==1.0.0 pywin32>=307 Pillow>=10.0.0 requests>=2.31.0 beautifulsoup4>=4.12.0 pystray>=0.19.0 weasyprint>=60.0 reportlab>=4.0.0
```

### Virtual Environment (Recommended)

To avoid dependency conflicts, use a virtual environment:

```bash
cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the client
python printer_client.py
```

## Configuration

No additional configuration is needed. The HTML printing feature is automatically enabled once the dependencies are installed.

### Optional: Configure PDF Page Size

To customize the PDF page size for your printers, edit `printer_handler.py`:

```python
# Line ~340 in printer_handler.py
custom_css = CSS(string='''
    @page {
        size: 80mm auto;  # Change to your printer width
        margin: 0;
        padding: 0;
    }
    body {
        margin: 0;
        padding: 5mm;
        font-family: Arial, sans-serif;
    }
''')
```

Common sizes:
- `80mm auto` - Standard thermal receipt printer (default)
- `58mm auto` - Small thermal printer
- `A4` - Standard paper
- `letter` - US letter size

## Verification Checklist

After installation, verify:

- [ ] `pip list` shows weasyprint and reportlab
- [ ] Client starts without errors
- [ ] Logs show "Auto-detected HTML content" when HTML is sent
- [ ] PDF files are created in temp directory
- [ ] PDF files are sent to printer
- [ ] Temporary files are cleaned up after printing
- [ ] SumatraPDF is installed (optional but recommended)

## Updating from Previous Version

If you're updating from a previous version:

1. **Backup your configuration**:
   ```bash
   copy .env .env.backup
   copy printer_settings.json printer_settings.json.backup
   ```

2. **Pull the latest code** (if using git):
   ```bash
   git pull origin main
   ```

3. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Restart the service**

## Build Executable (Optional)

If you want to rebuild the executable with the new features:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller PrintClientPro.spec --clean --noconfirm
```

The executable will be in the `dist` folder.

## Getting Help

If you encounter issues:

1. **Check the logs**: `printer_client.log` in the installation directory
2. **Review the HTML Printing Guide**: `HTML_PRINTING_GUIDE.md`
3. **Test with simple HTML** first before complex receipts
4. **Verify all dependencies** are installed correctly

## Next Steps

Once installed, refer to:
- **HTML_PRINTING_GUIDE.md** - Comprehensive guide for using HTML printing
- **README.md** - General application documentation

---

**Installation Complete!** You can now send HTML content and it will be printed as beautifully formatted PDFs. 🎉
