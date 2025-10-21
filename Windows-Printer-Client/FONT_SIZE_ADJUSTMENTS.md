# Font Size Adjustments and Separation Lines

## Summary

Reduced font sizes for title, company name, NIPT, and address to make receipts more compact and professional. Added proper separation lines for regular receipts (Fature Tatimore) while keeping Urdhri Punes clean.

## Changes Made

### 1. ReportLab Font Size Overrides (Lines 491-500)

Added font size overrides to make header elements smaller:

```python
# Override font sizes for specific classes to make them smaller
font_size_overrides = {
    'title1': '14px',          # Fature Tatimore - smaller (was 20px)
    'title1_urdhri': '14px',   # Urdhri titles - smaller (was 20px)
    'tds-footer': '11px',      # Company, NIPT, Address - smaller (was 18px)
}
```

**Font Size Changes:**
- **Title** (Fature Tatimore): 20px → **14px** (30% reduction)
- **Company Name** (Parid Smart Solution): 18px → **11px** (39% reduction)
- **NIPT** (L92119032V): 18px → **11px** (39% reduction)
- **Address** (Rr. Abdyl Frasheri...): 18px → **11px** (39% reduction)

### 2. Separation Lines for Regular Receipts (Lines 652-661)

Updated line rendering logic:

**Before:**
```python
if is_line_only_row:
    # Remove ALL dashed lines in ReportLab
    continue
```

**After:**
```python
if is_line_only_row:
    # For Fature Tatimore: Keep separation lines after header info
    # For Urdhri Punes: Remove all dashed lines
    if not is_urdhri_punes:
        # Draw a subtle separation line for regular receipts
        y -= 1 * mm
        c.setLineWidth(0.3)
        c.line(margin, y, width - margin, y)
        y -= 2 * mm
    continue
```

**Behavior:**
- ✓ **Fature Tatimore**: Shows thin separation lines (0.3mm width)
- ✓ **Urdhri Punes**: No separation lines (clean layout)
- ✓ Proper spacing before (1mm) and after (2mm) lines

### 3. PrintDirectly.js Matching Updates

Updated frontend styles to match ReportLab:

**Lines 82-100:**
```javascript
.title1 {
  font-size: 14px !important;  // Changed from 20px
  text-align: center !important;
  font-weight: bold !important;
}

.tds-footer{
  font-size: 11px !important;  // Changed from 18px
  font-weight: bold !important;
  text-align: center !important;
  width: 100% !important;
  margin: 0;
}

.title1_urdhri {
  font-size: 14px !important;  // Changed from 20px
  text-align: center !important;
  font-weight: bold !important;
}
```

## Visual Comparison

### Before:
```
Fature Tatimore          (20px - too large)
Parid Smart Solution     (18px - too large)
L92119032V               (18px - too large)
Rr. Abdyl Frasheri...    (18px - too large)

[No separation lines]
```

### After:
```
Fature Tatimore          (14px - compact)
Parid Smart Solution     (11px - compact)
L92119032V               (11px - compact)
Rr. Abdyl Frasheri...    (11px - compact)
_________________________
Data: Mon, 20 Oct 2025...
```

## Receipt Types

### Fature Tatimore (Regular Receipt)
- ✓ Smaller header fonts (14px title, 11px info)
- ✓ Separation lines after header
- ✓ Separation lines before column headers
- ✓ QR code rendered correctly
- ✓ Compact, professional layout

### Urdhri Punes (Work Order)
- ✓ Smaller header fonts (14px title, 11px info)
- ✓ NO separation lines (except around column headers)
- ✓ Solid lines before/after column headers only
- ✓ Clean, minimal layout

## Files Modified

### Backend (Windows-Printer-Client)
1. **printer_handler.py**
   - Lines 491-500: Font size overrides
   - Lines 652-661: Separation line logic

### Frontend (Paridi)
2. **PrintDirectly.js**
   - Lines 82-100: Updated CSS font sizes

## Testing

Run the test to verify changes:
```bash
cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
.\venv\Scripts\python.exe test_qr_code.py
```

Expected output:
- ✓ Smaller, more compact header
- ✓ Proper separation lines
- ✓ QR code in correct position
- ✓ Professional appearance

## Benefits

1. **More Compact** - 30-39% smaller header text saves vertical space
2. **Professional** - Cleaner, less overwhelming appearance
3. **Consistent** - HTML preview matches printed output exactly
4. **Readable** - Still legible at smaller sizes
5. **Space Efficient** - More content fits on receipt without scrolling

## Preview vs Print

Both now show:
- ✓ Same font sizes (14px title, 11px info)
- ✓ Same separation lines
- ✓ Same QR code placement
- ✓ Same overall layout

**Perfect match between preview and print!**
