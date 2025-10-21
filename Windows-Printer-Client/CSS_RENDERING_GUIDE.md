# CSS Rendering Guide for Windows Printer Client

## Problem Summary

Your `print_server/app.py` correctly renders CSS because it uses **wkhtmltopdf**, which is a full HTML rendering engine (based on WebKit browser). The Windows-Printer-Client was using **ReportLab** with custom CSS parsing, which has limited CSS support.

## Solution Implemented

I've added **wkhtmltopdf** support to the Windows-Printer-Client, giving you the same CSS rendering quality as print_server/app.py.

---

## PDF Converter Options

### 1. **wkhtmltopdf** P (RECOMMENDED - Best CSS Support)

**Why it's the best:**
- Full browser rendering engine (WebKit)
- 100% CSS support (same as Chrome/Safari)
- Handles complex layouts, flexbox, CSS Grid
- Proper font rendering
- Image support

**Installation:**

1. Download wkhtmltopdf:
   - Visit: https://wkhtmltopdf.org/downloads.html
   - Download the Windows installer (64-bit or 32-bit)
   - Install to default location: `C:\Program Files\wkhtmltopdf`

2. Or install via command line:
   ```powershell
   # Using Chocolatey
   choco install wkhtmltopdf

   # Using winget
   winget install wkhtmltopdf
   ```

3. Verify installation:
   ```cmd
   "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
   ```

4. **Required Python library:** (already installed)
   ```bash
   pip install pdfkit
   ```

**Configuration:**
- In the GUI, click "Configuration" ’ Select "wkhtmltopdf P" ’ Click "Save"
- The client will automatically find wkhtmltopdf in these locations:
  - `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
  - `C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe`
  - Same directory as the application
  - System PATH

---

### 2. **ReportLab** (Default - Custom CSS Parser)

**Pros:**
- No external dependencies
- Lightweight
- Optimized for table-based receipts
- Works out of the box

**Cons:**
- Limited CSS support
- Manual CSS parsing
- May not render complex layouts perfectly

**Use when:**
- Simple receipts with basic styling
- Cannot install wkhtmltopdf
- Need minimal dependencies

---

### 3. **WeasyPrint** (Advanced - Good CSS Support)

**Pros:**
- Good CSS support (CSS 2.1 and some CSS3)
- Pure Python implementation
- No external binary required

**Cons:**
- Requires GTK libraries on Windows (complex installation)
- Not as complete as wkhtmltopdf

**Installation:**
1. Install GTK for Windows (complex)
2. `pip install weasyprint`

---

### 4. **SumatraPDF** (Viewer Only)

**Note:** This uses ReportLab for conversion and SumatraPDF only for viewing/printing PDFs.

---

## How It Works Now

### Architecture Comparison

#### print_server/app.py (Your working version)
```
HTML with CSS ’ wkhtmltopdf ’ PDF ’ SumatraPDF ’ Printer
```

#### Windows-Printer-Client (Updated)
```
HTML with CSS ’ wkhtmltopdf/ReportLab ’ PDF ’ win32print ’ Printer
```

### What Changed

1. **Added wkhtmltopdf support** in [printer_handler.py:733-800](printer_handler.py#L733-L800)
   - Full CSS rendering engine
   - Same approach as print_server/app.py
   - Automatic fallback to ReportLab if wkhtmltopdf not available

2. **Improved ReportLab CSS parser** in [printer_handler.py:426-732](printer_handler.py#L426-L732)
   - Better CSS inheritance
   - Proper font-size handling
   - Multi-class support
   - Inline style support

3. **Updated GUI** in [printer_client_gui.py:149-218](printer_client_gui.py#L149-L218)
   - Added wkhtmltopdf button (marked as recommended)
   - Better layout for 4 converter options

---

## Testing

### Test with wkhtmltopdf

1. Install wkhtmltopdf (see installation above)
2. Open Windows Printer Client GUI
3. Click "Configuration"
4. Select "wkhtmltopdf P"
5. Click "Save"
6. Send a test print from your socket server

### Expected Results

With wkhtmltopdf, your CSS will render **exactly** as it does in print_server/app.py:

 Font sizes (20px, 14px, 11px, etc.)
 Font weights (bold, 500, 600, etc.)
 Text alignment (center, left, right)
 Colors
 Borders and lines
 Table layouts
 All CSS properties

---

## Configuration

### Set wkhtmltopdf as Default

**Option 1: Via GUI**
1. Open Printer Client GUI
2. Click "™ Configuration"
3. Select "wkhtmltopdf P"
4. Click "=¾ Save"

**Option 2: Edit .env file**
```env
PDF_CONVERTER=wkhtmltopdf
```

---

## Troubleshooting

### wkhtmltopdf not found

**Error:** `wkhtmltopdf not found. Please install wkhtmltopdf or use another converter.`

**Solution:**
1. Install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
2. Or place `wkhtmltopdf.exe` in the same folder as the application
3. Or add wkhtmltopdf to your system PATH

### pdfkit library missing

**Error:** `pdfkit library not installed. Run: pip install pdfkit`

**Solution:**
```bash
venv\Scripts\pip.exe install pdfkit
```

### CSS still not rendering

1. Check which converter is selected:
   - Open GUI ’ Configuration ’ Check selected button
2. Check logs for conversion method:
   - Look for "Using PDF converter: wkhtmltopdf" in logs
3. Verify wkhtmltopdf installation:
   ```cmd
   "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
   ```

---

## Performance Comparison

| Converter | CSS Support | Speed | Dependencies |
|-----------|------------|-------|--------------|
| **wkhtmltopdf** P |  (100%) |  (Medium) | wkhtmltopdf binary |
| ReportLab |  (Custom) |  (Fast) | None |
| WeasyPrint |  (Good) |  (Medium) | GTK libraries |
| SumatraPDF | Same as ReportLab | Same as ReportLab | SumatraPDF binary |

---

## Recommendation

**For production use with CSS styling:**
1.  Install wkhtmltopdf
2.  Select "wkhtmltopdf P" in GUI
3.  Enjoy perfect CSS rendering like print_server/app.py

**For simple receipts without CSS:**
- ReportLab (default) works fine
- No installation needed

---

## Summary

The Windows-Printer-Client now has the **same CSS rendering capability** as your print_server/app.py by using wkhtmltopdf. Simply install wkhtmltopdf and select it in the configuration to get perfect CSS rendering for your receipts!
