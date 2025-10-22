# Fature Porosi - Artikull Text Wrapping Fix

## Problem
"Fature Porosi" (Work Order) receipts have a 2-column table format (Sasia + Artikull), and long article names were being cut off without word wrapping.

## Example HTML Structure
```html
<thead>
  <tr>
    <th>Sasia</th>
    <th>Artikull</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="columnsPershkrim_urdhri">1 x </td>
    <td class="columnsPershkrim_urdhri">ZOG FSHATI TIK-TIK NEW (PLACK)yy sas</td>
  </tr>
</tbody>
```

## Solution

Modified `printer_handler.py` - `_convert_receipt_html_to_pdf()` function:

### Added Word Wrapping for 2-Column Fature Porosi Tables (Lines 850-904)

```python
# Check if this is a Fature Porosi table (Sasia + Artikull)
# Detect by checking if left text contains "x" (quantity marker)
is_fature_porosi = 'x' in left_text.lower() and not has_heading

if is_fature_porosi and is_tbody_row:
    # Calculate column widths: 20% for Sasia, 80% for Artikull
    sasia_width = (width - 2 * margin) * 0.2
    artikull_width = (width - 2 * margin) * 0.8

    # Draw Sasia (left column)
    c.drawString(margin, y, left_text)

    # Check if Artikull text fits in one line
    artikull_x = margin + sasia_width
    text_width = c.stringWidth(right_text, font_name, font_size)

    if text_width <= (artikull_width - 2*mm):
        # Fits in one line
        c.drawString(artikull_x, y, right_text)
    else:
        # Word wrap across multiple lines
        # Split into words and wrap to fit column width
        # Draw first line, then draw remaining lines indented
```

### Detection Logic
- **Identifies Fature Porosi tables** by checking if left column contains "x" (quantity marker like "1 x", "2 x")
- **Distinguishes from other 2-column tables** like TOTALI row (which has heading)
- **Only applies to tbody rows** (product rows, not headers)

### Column Width Allocation
- **Sasia (Quantity):** 20% of available width
- **Artikull (Article):** 80% of available width
- Padding: 2mm reserved for spacing

### Word Wrapping Algorithm
1. Calculate if text fits in one line
2. If fits → Draw normally on one line
3. If doesn't fit:
   - Split text into words
   - Build lines that fit within column width
   - Draw first line aligned with Sasia column
   - Draw remaining lines indented under Artikull column
   - Proper line spacing (font_size * 0.35 + 0.8mm)

### Added Spacing (Line 903-904)
```python
# Add extra spacing after Fature Porosi product row
y -= 2 * mm  # Extra spacing between products
```

## Visual Results

**Before:**
```
Sasia    Artikull
1 x      ZOG FSHATI TIK-TIK...  ← Text cut off
```

**After:**
```
Sasia    Artikull
1 x      ZOG FSHATI TIK-TIK NEW
         (PLACK)yy sas  ← Wrapped to next line

         ↑ 2mm spacing
```

## Testing

Example long article name:
```
"ZOG FSHATI TIK-TIK NEW (PLACK)yy sas"
```

Expected result:
- Line 1: "1 x      ZOG FSHATI TIK-TIK NEW"
- Line 2: "         (PLACK)yy sas"
- 2mm spacing after the product

## Configuration

Works automatically when:
- Printing "Fature Porosi" (Work Order) receipts
- Using ReportLab PDF converter
- 2-column table with Sasia + Artikull format

## Benefits

✅ **Complete text display** - No truncation of article names
✅ **Professional appearance** - Clean word wrapping
✅ **Proper spacing** - 2mm between products for readability
✅ **Flexible layout** - Adapts to any article name length
✅ **Maintains structure** - Sasia column stays aligned

## Files Modified

- `printer_handler.py` (lines 850-904)

## Related Fixes

This complements previous fixes:
1. 4-column table word wrapping (full invoices)
2. Solid lines after Tavolina/Menyra e Pageses
3. Spacing between product rows

## Backwards Compatibility

✅ 100% backwards compatible
✅ Only affects Fature Porosi format
✅ Other receipt types unchanged
✅ No breaking changes

---

**Date:** 2025-10-21
**Modified:** printer_handler.py (lines 850-904)
**Receipt Type:** Fature Porosi (Work Order)
**Format:** 2-column (Sasia + Artikull)
