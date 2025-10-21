"""
Test script to verify HTML printing with CSS styling
"""
import sys
import os

# Test HTML content with the same structure as your socket data
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

  .solid-line {
    border: 1.5px solid #000 !important;
    color: #000;
  }

  .div_line {
    width: 100%;
    height: 1px;
    background-color: #000;
    margin: 2px 0;
  }

  .line {
    font-weight: 500 !important;
    border-top: 2px solid black !important;
    color: #000 !important;
    width: 100% !important;
    margin: 0 !important;
  }

  hr {
    border-top: 1.5px dashed rgb(0, 0, 0);
    color: #000;
  }

  .columns {
    font-size: 11.5px !important;
    color: #000;
    text-align: right !important;
  }

  .columnsSkontrino_urdhri {
    font-weight: 600 !important;
    color: #000;
  }

  .columnsSkontrino {
    font-weight: 500 !important;
    font-size: 11px !important;
    color: #000;
  }

  .columnsFis {
    font-weight: 400 !important;
    font-size: 11px !important;
    color: #000;
  }

  .columnsTotal {
    padding-top: 20px;
    font-size: 14px !important;
    color: #000;
  }

  .columnsPershkrim_urdhri {
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #000;
  }

  .columnsPershkrim {
    font-weight: 600 !important;
    font-size: 11px !important;
    color: #000;
  }
  .columnsVlera {
    font-weight: 500 !important;
    font-size: 11px !important;
    color: #000;
    text-align: center !important;
  }
  .columnsvleracenterXhiroTurniPOS {
    text-align: right !important;
  }
  .columnsvleracenter {
    text-align: center !important;
  }

  .pershkrim {
    color: #000;
    font-size: 9.5px !important;
  }

  th {
    font-size: 12px !important;
  }

  tr {
    font-size: 12px !important;
    color: #000;
  }

  thead tr th {
    font-size: 12px !important;
  }

  td {
    font-size: 12px !important;
    color: #000;
  }
  .center-text {
    text-align: center;
  }

  thead {
    display: table-row-group;
    color: #000;
  }

  tfoot{
    text-align: center !important;
  }

  .footer {
    text-align: center !important;
  }

      </style>
    </head>
    <body>
      <div class="print"><table class="hide-border"><thead><tr><td class="title1" colspan="2"><h1>Fature</h1></td></tr><tr><td class="center-text" colspan="2">Parid Smart Solution</td></tr><tr><td class="center-text" colspan="2">L92119032V</td></tr><tr><td class="center-text" colspan="2">Rr. Abdyl Frasheri Tek Hekla Center</td></tr><tr><td class="center-text" colspan="2">+355 68 600 5012</td></tr><tr><td class="center-text" colspan="2">+355 68 600 5013</td></tr><tr><td colspan="2"><hr class="dashed-line"></td></tr><tr><td class="columnsSkontrino" colspan="2">Fature: 114</td></tr><tr><td class="columnsSkontrino" colspan="2">Data: Fri, 17 Oct 2025 00:00:00 GMT</td></tr><tr><td class="columnsSkontrino" colspan="2">Operator: A</td></tr><tr><td class="columnsSkontrino" colspan="2">Tavolina: 6</td></tr><tr><td class="columnsSkontrino" colspan="2">Menyra e Pageses: KESH i plote</td></tr></thead><tbody><tr><td colspan="2"><hr class="dashed-line"></td></tr></tbody></table><table class="hide-border"><thead><tr class="table-head" style="text-align: center;"><th class="th">Artikull</th><th class="th">Sasia</th><th class="th">Cmimi</th><th class="th">Vlera</th></tr></thead><tr><td colspan="5"><div class="div_line"></div></td></tr><tbody><tr><td class="columnsPershkrim">Artikull X</td><td class="columnsPershkrim">1 x</td><td class="columnsPershkrim">5,000</td><td class="columnsVlera">5,000</td></tr><tr><td colspan="4"><div class="dashed-line"></div></td></tr></tbody><tr><td class="columnsTotal flex-col" colspan="1"><h1>TOTALI</h1></td><td colspan="2"></td><td class="columnsTotal columnsvleracenter" colspan="3"><h1>5,000</h1></td><td colspan="4"></td></tr><tfoot><tr><td colspan="5"><div class="dashed-line"></div></td></tr><tr><td colspan="5">Gjeneruar nga Parid Smart Solution</td></tr></tfoot></table></div>
    </body>
    </html>
  """

# Create test data
test_data = {
    'type': 'html',
    'document_name': 'Test Invoice',
    'content': test_html  # This is how the socket sends it
}

# Test the printer handler
try:
    from printer_handler import PrinterHandler

    printer_handler = PrinterHandler()
    print(f"Default printer: {printer_handler.default_printer}")
    print("\nTesting HTML print with CSS...")
    print("-" * 50)

    result = printer_handler.print_document(test_data, printer_handler.default_printer)

    if result:
        print(" HTML print test successful!")
    else:
        print("L HTML print test failed - check the queue")

except Exception as e:
    print(f"L Error testing HTML print: {str(e)}")
    import traceback
    traceback.print_exc()
