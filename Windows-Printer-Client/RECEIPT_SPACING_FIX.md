# Receipt Spacing and Line Improvements

## Changes Made (October 21, 2025)

### Problem
Receipts were missing solid black separator lines and proper spacing in key locations:
1. No line after "Tavolina" field (red arrow in image 1)
2. No line after "Menyra e Pageses" field (red arrow in image 2)
3. Insufficient spacing between product rows (green arrows in image 2)

### Solution

Modified `printer_handler.py` - `_convert_receipt_html_to_pdf()` function:

#### 1. Added Line After "Tavolina" and "Menyra e Pageses" (Lines 789-796)

```python
# Check if this is "Tavolina" or "Menyra e Pageses" field - add line AFTER
# This check must be AFTER drawing text and spacing
if 'Tavolina:' in text or 'Menyra e Pageses:' in text:
    # Add spacing and solid line AFTER Tavolina/Menyra e Pageses
    y -= 1 * mm  # Extra space before line
    draw_solid_line(y)
    y -= 2 * mm  # Space after line
    last_section = 'after_tavolina'
```

**What it does:**
- Detects when rendering "Tavolina:" or "Menyra e Pageses:" fields
- Adds 1mm spacing before the line
- Draws a solid black line (1px / 0.5mm width)
- Adds 2mm spacing after the line
- Sets tracking flag to avoid duplicate lines

#### 2. Added Extra Spacing After Product Rows (Lines 952-954)

```python
# Add extra spacing after product row if in tbody
if is_tbody_row:
    y -= 2 * mm  # Extra spacing between products (green arrows in image)
```

**What it does:**
- Detects when a row is in `<tbody>` (product row)
- Adds 2mm extra spacing after each product
- Makes receipts more readable with clear separation between items

### Visual Results

**Before:**
```
Tavolina:37
Sasia    Artikull
```

**After:**
```
Tavolina:37
─────────────── (solid black line)
Sasia    Artikull
```

**Before (products):**
```
Pizza Margherita    1x    5.00    5.00
Kafe Espresso       2x    2.50    5.00
```

**After (products):**
```
Pizza Margherita    1x    5.00    5.00

Kafe Espresso       2x    2.50    5.00
    ↑ (2mm extra spacing)
```

### Files Modified

- `printer_handler.py` (lines 789-796, 952-954)

### Testing

To test locally:
```bash
venv\Scripts\python.exe printer_client_gui.py
```

Then print:
1. **Fature Porosi** (Work Order) - Check line after "Tavolina"
2. **Full Invoice** - Check line after "Menyra e Pageses" and spacing between products

### Configuration

Works automatically when:
- `.env` has `PDF_CONVERTER=reportlab`
- OR wkhtmltopdf fails and falls back to ReportLab
- OR user selects ReportLab in GUI Configuration

### Backwards Compatibility

✅ Fully backwards compatible
✅ Only adds visual improvements
✅ No breaking changes
✅ Works with all receipt types

### Related Changes

This builds on previous fixes:
- Artikull text wrapping (prevents truncation)
- Solid lines at strategic positions (professional appearance)
- Proper spacing (improved readability)

---

**Date:** 2025-10-21
**Modified:** printer_handler.py (lines 789-796, 952-954)
**Tested:** ReportLab PDF renderer
