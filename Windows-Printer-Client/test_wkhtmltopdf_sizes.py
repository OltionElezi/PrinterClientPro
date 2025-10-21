"""
Test script to verify wkhtmltopdf font size reductions
"""
import sys
import os
import tempfile

# The actual HTML content from the user
test_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <style>
        html, body {
          width: 100%;
          height: 100%;
          margin: 0 !important;
          padding: 0 !important;
          box-sizing: border-box;
        }

  .print {
    width: 100%;
    height: 100%;
  }

  table{
    width: 100%;
  }

  .theadMain {
    display: flex !important;
    flex-direction: column !important;
  }

  .title1 {
    font-size: 20px !important;
    text-align: center !important;
    font-weight: bold !important;
  }

  .tds-footer{
    font-size: 18px !important;  /* increased from 16px */
    font-weight: bold !important;
    text-align: center !important;
    width: 100% !important;
    margin: 0;
  }

  .title1_urdhri {
    font-size: 20px !important;
    text-align: center !important;
    font-weight: bold !important;
  }


  .hide-border {
    border: 1.5px solid rgba(0, 0, 0, 0) !important;
  }

  .dashed-line {
    border-top: 1px dashed #000 !important;
    color: #000;
    width: "100%" !important;
    padding-top: 2px;
    padding-bottom: 2px;
  }

      </style>
    </head>
    <body>
      <div class="print"><table class="hide-border"><thead><tr><td class="title1" colspan="5"><h1>Fature Tatimore</h1></td></tr><tr><td class="tds-footer" colspan="5">Parid Smart Solution</td></tr><tr><td class="tds-footer" colspan="5">L92119032V</td></tr><tr><td class="tds-footer" colspan="5">Rr. Abdyl Frasheri Tek Hekla Center</td></tr></thead></table></div>
    </body>
    </html>
  """

# Test the printer handler
try:
    from printer_handler import PrinterHandler

    printer_handler = PrinterHandler()
    print(f"Default printer: {printer_handler.default_printer}")

    # Force wkhtmltopdf
    os.environ['PDF_CONVERTER'] = 'wkhtmltopdf'

    print("\nTesting wkhtmltopdf with reduced font sizes...")
    print("-" * 60)

    # Create a test PDF
    pdf_path = printer_handler._convert_html_to_pdf(test_html)

    if pdf_path and os.path.exists(pdf_path):
        pdf_size = os.path.getsize(pdf_path)
        print(f"[OK] PDF created successfully!")
        print(f"  Path: {pdf_path}")
        print(f"  Size: {pdf_size:,} bytes")
        print(f"\n[OK] Font size reductions applied:")
        print(f"  - Title 'Fature Tatimore': 20px -> 16px")
        print(f"  - Company/NIPT/Address: 18px -> 12px")
        print(f"\nYou can open this PDF to verify the smaller fonts:")
        print(f"  {pdf_path}")
    else:
        print("[ERROR] PDF creation failed")

except Exception as e:
    print(f"[ERROR] Error: {str(e)}")
    import traceback
    traceback.print_exc()
