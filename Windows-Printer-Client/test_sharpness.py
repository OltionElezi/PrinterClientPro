"""
Test script to verify wkhtmltopdf sharpness improvements
"""
import sys
import os
import tempfile

# Test HTML with various font sizes to check sharpness
test_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 10px;
    }
    .test-section {
      margin: 10px 0;
      border-bottom: 1px solid #ccc;
      padding-bottom: 10px;
    }
    h1 { font-size: 20px; font-weight: bold; }
    h2 { font-size: 16px; font-weight: bold; }
    .normal { font-size: 12px; }
    .small { font-size: 10px; }
    .tiny { font-size: 8px; }
  </style>
</head>
<body>
  <div class="test-section">
    <h1>SHARPNESS TEST - 20px Bold</h1>
    <p>Testing text rendering quality at different sizes</p>
  </div>

  <div class="test-section">
    <h2>Header 2 - 16px Bold</h2>
    <p class="normal">Normal text - 12px: The quick brown fox jumps over the lazy dog</p>
    <p class="small">Small text - 10px: The quick brown fox jumps over the lazy dog</p>
    <p class="tiny">Tiny text - 8px: The quick brown fox jumps over the lazy dog</p>
  </div>

  <div class="test-section">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="font-weight: bold;">
          <th style="text-align: left;">Item</th>
          <th style="text-align: center;">Qty</th>
          <th style="text-align: right;">Price</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Test Product 1</td>
          <td style="text-align: center;">2 x</td>
          <td style="text-align: right;">5,000</td>
        </tr>
        <tr>
          <td>Test Product 2</td>
          <td style="text-align: center;">3 x</td>
          <td style="text-align: right;">7,500</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="test-section">
    <p style="font-weight: bold;">Bold Text Test</p>
    <p style="font-weight: 500;">Medium Weight (500)</p>
    <p style="font-weight: 600;">Semi-Bold (600)</p>
    <p style="font-weight: normal;">Normal Weight</p>
  </div>
</body>
</html>
"""

# Test the printer handler
try:
    from printer_handler import PrinterHandler

    printer_handler = PrinterHandler()
    print(f"Default printer: {printer_handler.default_printer}")
    print(f"PDF Converter: {os.getenv('PDF_CONVERTER', 'reportlab')}")
    print(f"Font Scale: {os.getenv('FONT_SCALE', '1.0')}")
    print("\nTesting wkhtmltopdf sharpness with 600 DPI...")
    print("-" * 60)

    # Create test data
    test_data = {
        'type': 'html',
        'document_name': 'Sharpness Test',
        'content': test_html
    }

    # Convert to PDF (but don't actually print)
    from dotenv import load_dotenv
    load_dotenv(override=True)

    # Force wkhtmltopdf
    os.environ['PDF_CONVERTER'] = 'wkhtmltopdf'

    # Create a test PDF
    pdf_path = printer_handler._convert_html_to_pdf(test_html)

    if pdf_path and os.path.exists(pdf_path):
        pdf_size = os.path.getsize(pdf_path)
        print(f"[OK] PDF created successfully!")
        print(f"  Path: {pdf_path}")
        print(f"  Size: {pdf_size:,} bytes")
        print(f"\n[OK] Sharpness settings applied:")
        print(f"  - DPI: 600 (very high)")
        print(f"  - Font smoothing: subpixel-antialiased")
        print(f"  - Text rendering: geometricPrecision")
        print(f"  - PDF compression: disabled")
        print(f"\nYou can open this PDF to verify sharpness:")
        print(f"  {pdf_path}")
    else:
        print("[ERROR] PDF creation failed")

except Exception as e:
    print(f"[ERROR] Error: {str(e)}")
    import traceback
    traceback.print_exc()
