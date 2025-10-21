"""
Test script to verify ReportLab modifications:
- All dashed lines removed
- Solid lines before/after headers only for urdhri punes
"""
import sys
import os

# Test HTML for regular receipt (Fature Tatimore)
fature_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    .title1 { font-size: 20px !important; text-align: center !important; font-weight: bold !important; }
    .tds-footer { font-size: 18px !important; font-weight: bold !important; text-align: center !important; }
    .hide-border { border: 1.5px solid rgba(0, 0, 0, 0) !important; }
    .dashed-line { border-top: 1px dashed #000 !important; }
    .columnsPershkrim { font-weight: 600 !important; font-size: 11px !important; }
    .columnsVlera { font-weight: 500 !important; font-size: 11px !important; text-align: center !important; }
    .columnsTotal { padding-top: 20px; font-size: 14px !important; }
  </style>
</head>
<body>
  <div class="print">
    <table class="hide-border">
      <thead>
        <tr><td class="title1" colspan="5"><h1>Fature Tatimore</h1></td></tr>
        <tr><td class="tds-footer" colspan="5">Parid Smart Solution</td></tr>
        <tr><td colspan="5"><div class="dashed-line"></div></td></tr>
      </thead>
    </table>
    <table class="hide-border">
      <thead>
        <tr class="table-head" style="text-align: center;">
          <th class="th">Artikull</th>
          <th class="th">Sasia</th>
          <th class="th">Cmimi</th>
          <th class="th">Vlera</th>
        </tr>
      </thead>
      <tr><td colspan="5"><div class="dashed-line"></div></td></tr>
      <tbody>
        <tr>
          <td class="columnsPershkrim">Kafe</td>
          <td class="columnsPershkrim">1 x</td>
          <td class="columnsPershkrim">80</td>
          <td class="columnsVlera">80</td>
        </tr>
      </tbody>
      <tr><td colspan="5"><div class="dashed-line"></div></td></tr>
      <tr>
        <td class="columnsTotal" colspan="1"><h1>Totali</h1></td>
        <td class="columnsTotal" colspan="3"><h1>80</h1></td>
      </tr>
    </table>
  </div>
</body>
</html>
"""

# Test HTML for urdhri punes
urdhri_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    .title1 { font-size: 20px !important; text-align: center !important; font-weight: bold !important; }
    .tds-footer { font-size: 18px !important; font-weight: bold !important; text-align: center !important; }
    .hide-border { border: 1.5px solid rgba(0, 0, 0, 0) !important; }
    .dashed-line { border-top: 1px dashed #000 !important; }
    .columnsPershkrim { font-weight: 600 !important; font-size: 11px !important; }
  </style>
</head>
<body>
  <div class="print">
    <table class="hide-border">
      <thead>
        <tr><td class="title1" colspan="5"><h1>Urdhri i Punes</h1></td></tr>
        <tr><td class="tds-footer" colspan="5">Tavolina: 5</td></tr>
        <tr><td colspan="5"><div class="dashed-line"></div></td></tr>
      </thead>
    </table>
    <table class="hide-border">
      <thead>
        <tr class="table-head" style="text-align: center;">
          <th class="th">Artikull</th>
          <th class="th">Sasia</th>
          <th class="th">Cmimi</th>
          <th class="th">Vlera</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="columnsPershkrim">Pizza</td>
          <td class="columnsPershkrim">2 x</td>
          <td class="columnsPershkrim">500</td>
          <td class="columnsPershkrim">1000</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""

try:
    from printer_handler import PrinterHandler

    # Force ReportLab
    os.environ['PDF_CONVERTER'] = 'reportlab'

    printer_handler = PrinterHandler()
    print(f"Default printer: {printer_handler.default_printer}")
    print(f"PDF Converter: {os.getenv('PDF_CONVERTER', 'reportlab')}")
    print("\n" + "="*60)

    # Test 1: Regular receipt (Fature Tatimore)
    print("\nTest 1: Regular Receipt (Fature Tatimore)")
    print("-" * 60)
    print("Expected: NO dashed lines anywhere")
    pdf_path1 = printer_handler._convert_html_to_pdf(fature_html)
    if pdf_path1 and os.path.exists(pdf_path1):
        print(f"[OK] PDF created: {pdf_path1}")
        print("     All dashed lines should be removed")
    else:
        print("[ERROR] PDF creation failed")

    print("\n" + "="*60)

    # Test 2: Urdhri Punes
    print("\nTest 2: Urdhri Punes (Work Order)")
    print("-" * 60)
    print("Expected: NO dashed lines, SOLID lines before/after column headers")
    pdf_path2 = printer_handler._convert_html_to_pdf(urdhri_html)
    if pdf_path2 and os.path.exists(pdf_path2):
        print(f"[OK] PDF created: {pdf_path2}")
        print("     Should have solid lines around column headers (Artikull, Sasia, etc.)")
    else:
        print("[ERROR] PDF creation failed")

    print("\n" + "="*60)
    print("\nSummary:")
    print("- Fature Tatimore: No dashed lines at all")
    print("- Urdhri Punes: Solid lines before & after column headers")

except Exception as e:
    print(f"[ERROR] Error: {str(e)}")
    import traceback
    traceback.print_exc()
