"""
Debug script to trace exactly what's happening with tax table rendering
"""
from bs4 import BeautifulSoup

# Simulate the HTML structure
html = """
<!DOCTYPE html>
<html>
<body>
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
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Simulate the rendering logic
last_section = None
table_num = 0

print("SIMULATING RENDERING LOGIC:")
print("=" * 70)

for table in soup.find_all('table'):
    table_num += 1
    print(f"\n>>> Processing TABLE {table_num}")
    row_num = 0

    for row in table.find_all('tr'):
        row_num += 1
        cells = row.find_all(['td', 'th'])

        if not cells:
            continue

        # Get cell texts
        non_empty_cells = [cell for cell in cells if cell.get_text().strip()]
        cell_texts = [cell.get_text().strip() for cell in non_empty_cells]

        if len(cells) < 2:
            print(f"  Row {row_num}: SINGLE CELL - {cell_texts}")
            continue

        # Multi-cell row
        print(f"  Row {row_num}: {cell_texts}")

        # NEW LOGIC: Check if this row contains tax keywords OR if we're inside tax table
        is_tax_table_row = any('TVSH' in text or 'Tipi' in text for text in cell_texts)
        is_inside_tax_table = last_section == 'tax_table_header'

        print(f"    is_tax_table_row = {is_tax_table_row}")
        print(f"    is_inside_tax_table = {is_inside_tax_table}")

        if is_tax_table_row or is_inside_tax_table:
            print(f"    last_section BEFORE = '{last_section}'")

            # Check if we should skip
            if last_section == 'tax_table_complete':
                print(f"    >>> SKIP: tax_table_complete")
                continue

            # Check if this is header
            is_tax_header = 'Tipi' in cell_texts and 'TVSH' in cell_texts
            print(f"    is_tax_header = {is_tax_header}")

            if is_tax_header:
                if last_section == 'tax_table_header' or last_section == 'tax_table_complete':
                    print(f"    >>> SKIP: duplicate header (last_section={last_section})")
                    continue

                print(f"    >>> RENDER: Tax table HEADER")
                last_section = 'tax_table_header'
            elif is_inside_tax_table:
                # Data row
                print(f"    >>> RENDER: Tax table DATA row")
                last_section = 'tax_table_complete'

            print(f"    last_section AFTER = '{last_section}'")

print("\n" + "=" * 70)
print(f"Final state: last_section = '{last_section}'")
print("=" * 70)
