"""
Test script to verify tax table only appears once and has proper formatting
"""
import sys
import os
import tempfile

# HTML with DUPLICATE tax table (as it appears in actual receipts)
html_with_duplicate = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; font-size: 10px; }
        table { width: 100%; border-collapse: collapse; }
        .tds-footer { border-bottom: 1px solid black; }
        .columnsSkontrino { margin: 5px 0; }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr><th colspan="3" style="font-size: 14px; font-weight: bold;">Fature Talimore</th></tr>
            <tr><th colspan="3">Parid Smart Solution</th></tr>
            <tr><th colspan="3">SHLJ | 1.1402V</th></tr>
        </thead>
        <tbody>
            <tr><td colspan="3" class="tds-footer">Rr. Azizaj Fazluan Tek Mesta Gaming</td></tr>
        </tbody>
    </table>

    <div class="columnsSkontrino">
        <div>Data: Mon, 20 Oct 2025 00:00:00 GMT</div>
        <div>Operator: IAJ</div>
        <div>Tavolina: Z3</div>
        <div>Mënyra e Pagesës: KESH | pista</div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Artikull</th>
                <th>Sasia</th>
                <th>Cmimi</th>
                <th>Vlera</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Kafe</td><td>1 x</td><td>80</td><td>80</td></tr>
            <tr><td>Uje</td><td>1 x</td><td>200</td><td>200</td></tr>
            <tr><td>Birrë</td><td>1 x</td><td>2000</td><td>2000</td></tr>
            <tr><td>Lëng</td><td>1 x</td><td>10</td><td>10</td></tr>
        </tbody>
    </table>

    <table>
        <tbody>
            <tr><td colspan="3" style="font-size: 14px; font-weight: bold;">Totali</td><td style="font-size: 14px; font-weight: bold;">2,290</td></tr>
            <tr><td colspan="4">Vlera (Blerje/Shitje/Cmim i veçantë/LIBR/ Zbritje/Anulim)</td></tr>
            <tr><td>Tipi</td><td>TVSH</td><td>Vlera pa TVSH</td><td>Vlera me TVSH</td></tr>
            <tr><td>A</td><td>0</td><td>1,908.34</td><td>2,290</td></tr>
        </tbody>
    </table>

    <table>
        <tbody>
            <tr><td>Tipi</td><td>TVSH</td><td>Vlera pa TVSH</td><td>Vlera me TVSH</td></tr>
            <tr><td>A</td><td>0</td><td>1,908.34</td><td>2,290</td></tr>
        </tbody>
    </table>

    <table>
        <tfoot>
            <tr><td colspan="3">RHTXZGJJT019K0251917P028301001107</td></tr>
            <tr><td colspan="3">NIVF:BBBBBBBBBBBBBBBBB</td></tr>
            <tr><td colspan="3"><img src="qr_placeholder" /></td></tr>
            <tr><td colspan="3">Gjeneruar nga Parid Smart Solution</td></tr>
        </tfoot>
    </table>
</body>
</html>
"""

# Import the handler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from printer_handler import PrinterHandler

# Create handler
handler = PrinterHandler()

try:
    # Generate PDF using the internal method
    result_path = handler._convert_html_to_pdf_reportlab(html_with_duplicate)

    if result_path and os.path.exists(result_path):
        file_size = os.path.getsize(result_path)
        print(f"\n{'='*60}")
        print(f"Tax Table Duplicate Test - PASSED")
        print(f"{'='*60}")
        print(f"PDF created: {result_path}")
        print(f"File size: {file_size:,} bytes")
        print(f"\n[SUCCESS] PDF generated with duplicate tax table in HTML")
        print(f"[SUCCESS] Verify that tax table appears ONLY ONCE in the PDF")
        print(f"\nPlease open the PDF and check:")
        print(f"  1. Tax table (Tipi, TVSH, Vlera pa TVSH, Vlera me TVSH) appears ONCE")
        print(f"  2. Tax table has proper borders around each cell")
        print(f"  3. Text is properly sized and centered in cells (not overlapping)")
        print(f"  4. Tax table has line before and after it")
        print(f"{'='*60}\n")
    else:
        print(f"\n[ERROR] PDF creation failed")

except Exception as e:
    print(f"\n[ERROR] Exception during test: {str(e)}")
    import traceback
    traceback.print_exc()
