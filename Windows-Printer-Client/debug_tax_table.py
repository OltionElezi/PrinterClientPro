"""
Debug script to understand tax table duplication issue
"""
from bs4 import BeautifulSoup

# Sample HTML with tax table (similar to what PrintDirectly.js generates)
html_sample = """
<html>
<body>
<table>
<tr><td>Totali</td><td></td><td>2,290</td></tr>
<tr><td colspan="3">Vlera (Blerje/Shitje/Cmim i veçantë/LIBR/ Zbritje/Anulim)</td></tr>
<tr><td>Tipi</td><td>TVSH</td><td>Vlera pa TVSH</td><td>Vlera me TVSH</td></tr>
<tr><td>A</td><td>0</td><td>1,908.34</td><td>2,290</td></tr>
</table>

<div>Some other content</div>

<table>
<tr><td>Tipi</td><td>TVSH</td><td>Vlera pa TVSH</td><td>Vlera me TVSH</td></tr>
<tr><td>A</td><td>0</td><td>1,908.34</td><td>2,290</td></tr>
</table>
</body>
</html>
"""

soup = BeautifulSoup(html_sample, 'html.parser')
tables = soup.find_all('table')

print(f"Found {len(tables)} tables in HTML")
print("=" * 60)

for idx, table in enumerate(tables):
    print(f"\nTable {idx + 1}:")
    print("-" * 60)
    rows = table.find_all('tr')
    for row_idx, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        cell_texts = [cell.get_text(strip=True) for cell in cells]

        # Check if this is tax table
        is_tax = any('TVSH' in text or 'Tipi' in text for text in cell_texts)
        is_header = any('Artikull' in text or 'Sasia' in text or 'Tipi' in text for text in cell_texts)

        print(f"  Row {row_idx + 1}: {cell_texts}")
        print(f"    -> is_tax={is_tax}, is_header={is_header}")

print("\n" + "=" * 60)
print("Analysis: Looking for tax table patterns...")
print("=" * 60)

# Count how many times we see the tax table header
tax_header_count = 0
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        cell_texts = [cell.get_text(strip=True) for cell in cells]
        if 'Tipi' in cell_texts and 'TVSH' in cell_texts:
            tax_header_count += 1
            print(f"Found tax table header: {cell_texts}")

print(f"\nTotal tax table headers found: {tax_header_count}")
