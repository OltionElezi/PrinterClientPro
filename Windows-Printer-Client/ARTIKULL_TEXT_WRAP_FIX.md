# Artikull Column Text Wrapping Fix

## Problem
When using ReportLab as the PDF converter, long text in the "Artikull" (Article) column was being truncated or cut off. The text would not display fully on the receipt.

## Root Cause
1. **Optimized Receipt Renderer** (`_convert_receipt_html_to_pdf`):
   - Line 888: Text was drawn without considering if it exceeds column width
   - No word wrapping logic for long article names

2. **General ReportLab Renderer** (`_convert_html_to_pdf_reportlab`):
   - Line 1548: Used Python string formatting `{row_cells[0]['text']:<20}` which truncated text to 20 characters
   - This happened BEFORE the word-wrapping `add_text()` function could process it

## Solution

### For Optimized Receipt Renderer (Lines 881-941)
Added intelligent word wrapping for the Artikull column:

```python
# Calculate max width for Artikull column
max_artikull_width = col_width - 2*mm

# Check if text fits in one line
if text_width <= max_artikull_width:
    # Draw normally on one line
    c.drawString(x_pos_artikull, y, artikull_text)
else:
    # Wrap text across multiple lines
    # Split into words and wrap to fit column width
    # Draw first line with other columns (Sasia, Cmimi, Vlera)
    # Draw remaining lines below (Artikull column only)
```

**Benefits:**
- Full article names are always displayed
- Text wraps to multiple lines if needed
- Other columns (Sasia, Cmimi, Vlera) stay aligned on the first line
- Maintains table structure and readability

### For General ReportLab Renderer (Lines 1544-1566)
Removed truncation from string formatting:

**Before:**
```python
line = f"{row_cells[0]['text']:<20} {row_cells[1]['text']:>6}..."
# This truncated Artikull to 20 characters
```

**After:**
```python
artikull_full = row_cells[0]['text']  # No truncation
line = f"{artikull_full}  {sasia:>6} {cmimi:>8} {vlera:>8}"
# Full text preserved, add_text() handles word wrapping
```

**Benefits:**
- Full article names preserved
- Existing `add_text()` function handles word wrapping automatically
- Clean, maintainable code

## Testing

### Test Case 1: Short Article Name
```
Artikull: "Kafe"
Expected: Displays on one line
Result: ✓ Works correctly
```

### Test Case 2: Long Article Name
```
Artikull: "Kafe Espresso me Qumesht dhe Sheqer Ekstra"
Expected: Wraps to multiple lines, all text visible
Result: ✓ Works correctly
```

### Test Case 3: Very Long Article Name
```
Artikull: "Pizza Margherita me Mozzarella, Domate, Bozilok dhe Vaj Ulliri Ekstra Virgin"
Expected: Wraps to 3-4 lines, all text visible
Result: ✓ Works correctly
```

## Configuration
This fix works automatically when:
- `.env` has `PDF_CONVERTER=reportlab`
- OR when wkhtmltopdf fails and falls back to ReportLab
- OR when user explicitly selects ReportLab in GUI Configuration panel

## Files Modified
1. `printer_handler.py`:
   - Lines 881-941: Added word wrapping for optimized receipt renderer
   - Lines 1544-1566: Removed truncation from general ReportLab renderer

## Backwards Compatibility
✓ Fully backwards compatible
✓ No breaking changes
✓ Works with existing receipts
✓ Improves rendering quality

## Performance Impact
- Negligible (only affects multi-line article names)
- Word wrapping calculation is fast (milliseconds)
- No impact on single-line items

## Related Issues
- Fixes: Article names getting cut off in ReportLab mode
- Improves: Receipt readability and accuracy
- Maintains: Professional appearance of receipts

---

**Date:** 2025-10-21
**Fixed in:** printer_handler.py (lines 881-941, 1544-1566)
**Tested with:** ReportLab PDF renderer
