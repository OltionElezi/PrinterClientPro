"""
Printer Handler Module
Handles all printing operations for Windows
"""
import win32print
import win32ui
import win32con
from PIL import Image, ImageDraw, ImageFont
import logging
import json
from datetime import datetime
import tempfile
import os
import sys
import subprocess
import io
from config import Config

logger = logging.getLogger(__name__)

class PrinterHandler:
    def __init__(self):
        self.default_printer = win32print.GetDefaultPrinter()
        self.print_queue = []  # Queue for failed/pending prints
        logger.info(f"Default printer: {self.default_printer}")

    def get_available_printers(self):
        """Get list of available printers with status"""
        printers = []
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers_info = win32print.EnumPrinters(flags, None, 1)

        for printer in printers_info:
            printer_name = printer[2]
            status = self.get_printer_status(printer_name)
            printers.append({
                'name': printer_name,
                'status': status,
                'is_default': printer_name == self.default_printer
            })

        return printers

    def get_printer_status(self, printer_name):
        """Check if printer is online and ready"""
        try:
            handle = win32print.OpenPrinter(printer_name)
            printer_info = win32print.GetPrinter(handle, 2)

            # Check for jobs in Windows spooler queue
            try:
                jobs = win32print.EnumJobs(handle, 0, -1, 1)
                if jobs:
                    logger.info(f"Printer '{printer_name}' has {len(jobs)} jobs in Windows spooler")
            except:
                pass

            win32print.ClosePrinter(handle)

            status = printer_info['Status']
            if status == 0:
                return 'Ready'
            elif status & win32print.PRINTER_STATUS_OFFLINE:
                return 'Offline'
            elif status & win32print.PRINTER_STATUS_ERROR:
                return 'Error'
            elif status & win32print.PRINTER_STATUS_PAUSED:
                return 'Paused'
            elif status & win32print.PRINTER_STATUS_PAPER_JAM:
                return 'Paper Jam'
            elif status & win32print.PRINTER_STATUS_PAPER_OUT:
                return 'Paper Out'
            elif status & win32print.PRINTER_STATUS_OUTPUT_BIN_FULL:
                return 'Output Bin Full'
            else:
                return 'Unknown'
        except Exception as e:
            logger.error(f"Error checking printer status: {str(e)}")
            return 'Not Available'

    def find_printer(self, printer_name):
        """Find printer by name (case-insensitive, partial match)"""
        available_printers = self.get_available_printers()

        # Exact match first
        for printer in available_printers:
            if printer['name'].lower() == printer_name.lower():
                return printer['name']

        # Partial match
        for printer in available_printers:
            if printer_name.lower() in printer['name'].lower():
                return printer['name']

        return None

    def print_document(self, data, printer_name=None):
        """
        Print a document with given data
        Args:
            data: Dictionary containing print data
            printer_name: Name of the printer (optional, uses default if not specified)
        """
        try:
            if printer_name is None:
                printer_name = self.default_printer

            # Try to find the printer if not found exactly
            found_printer = self.find_printer(printer_name)

            if found_printer is None:
                # Printer not found - add to queue
                logger.warning(f"Printer '{printer_name}' not found. Adding to queue.")
                self.add_to_queue(data, printer_name)
                return False

            printer_name = found_printer

            # Check printer status before attempting to print
            status = self.get_printer_status(printer_name)
            logger.info(f"Printing to: {printer_name} (Status: {status})")

            if status not in ['Ready', 'Unknown']:
                logger.warning(f"Printer '{printer_name}' is not ready (Status: {status}). Adding to queue.")
                self.add_to_queue(data, printer_name)
                return False

            # Print based on data type
            print_type = data.get('type', 'text')

            # Special handling for HTML - convert to PDF first
            if print_type == 'html':
                # Add printer name to data for HTML printing
                data['printer_name'] = printer_name

                # For HTML, we don't use the device context, we convert to PDF and print directly
                html_content = data.get('html', data.get('content', ''))
                if html_content:
                    pdf_path = None
                    try:
                        # Convert HTML to PDF
                        logger.info("📄 Converting HTML to PDF...")
                        logger.info(f"   HTML length: {len(html_content)} characters")
                        pdf_path = self._convert_html_to_pdf(html_content)

                        if not pdf_path:
                            logger.error("❌ PDF conversion returned None")
                            raise Exception("Failed to create PDF from HTML - converter returned None")

                        if not os.path.exists(pdf_path):
                            logger.error(f"❌ PDF file not found at: {pdf_path}")
                            raise Exception(f"Failed to create PDF from HTML - file not found at {pdf_path}")

                        # Log PDF file details
                        pdf_size = os.path.getsize(pdf_path)
                        logger.info(f"✅ PDF created: {pdf_path} ({pdf_size} bytes)")

                        # Print the PDF file
                        logger.info(f"🖨️ Printing PDF to {printer_name}...")
                        result = self._print_pdf_file(pdf_path, printer_name)

                        if result:
                            logger.info("✅ HTML printed successfully via PDF conversion")
                            return True
                        else:
                            logger.error("❌ _print_pdf_file returned False")
                            raise Exception("Failed to print PDF")

                    finally:
                        # Clean up temporary PDF file
                        if pdf_path and os.path.exists(pdf_path):
                            try:
                                import time
                                time.sleep(2)
                                os.remove(pdf_path)
                                logger.info(f"Cleaned up temporary PDF: {pdf_path}")
                            except Exception as e:
                                logger.warning(f"Could not delete temporary PDF: {str(e)}")

            # For other types, use the device context
            # Get printer handle
            hprinter = win32print.OpenPrinter(printer_name)

            try:
                # Create a device context
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(printer_name)

                # Start the document
                doc_name = data.get('document_name', f'Print Job {datetime.now().strftime("%Y%m%d_%H%M%S")}')
                hdc.StartDoc(doc_name)
                hdc.StartPage()

                # Get page dimensions
                page_width = hdc.GetDeviceCaps(win32con.HORZRES)
                page_height = hdc.GetDeviceCaps(win32con.VERTRES)

                if print_type == 'text':
                    self._print_text(hdc, data, page_width, page_height)
                elif print_type == 'receipt':
                    self._print_receipt(hdc, data, page_width, page_height)
                elif print_type == 'reservation':
                    self._print_reservation(hdc, data, page_width, page_height)
                else:
                    # Default text printing
                    self._print_text(hdc, data, page_width, page_height)

                # End the page and document
                hdc.EndPage()
                hdc.EndDoc()

                logger.info(f"Print job completed successfully: {doc_name}")
                return True

            finally:
                hdc.DeleteDC()
                win32print.ClosePrinter(hprinter)

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"❌ Error printing document: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Full traceback:\n{error_details}")

            # Log additional context
            logger.error(f"Print context:")
            logger.error(f"  - Printer: {printer_name}")
            logger.error(f"  - Print type: {data.get('type', 'unknown')}")
            logger.error(f"  - Data keys: {list(data.keys())}")

            # Add to queue if printing failed
            logger.warning(f"Print failed for '{printer_name}'. Adding to queue.")
            self.add_to_queue(data, printer_name)
            return False

    def _print_text(self, hdc, data, page_width, page_height):
        """Print simple text content"""
        content = data.get('content', 'No content provided')

        # Set font
        font = win32ui.CreateFont({
            "name": "Arial",
            "height": 40,
            "weight": 400,
        })
        hdc.SelectObject(font)

        # Print text
        lines = content.split('\n')
        y_position = 100

        for line in lines:
            hdc.TextOut(100, y_position, line)
            y_position += 60

    def _print_receipt(self, hdc, data, page_width, page_height):
        """Print a receipt"""
        # Header
        header_font = win32ui.CreateFont({
            "name": "Arial",
            "height": 60,
            "weight": 700,
        })
        hdc.SelectObject(header_font)
        hdc.TextOut(100, 100, "RECEIPT")

        # Normal font for content
        normal_font = win32ui.CreateFont({
            "name": "Arial",
            "height": 40,
            "weight": 400,
        })
        hdc.SelectObject(normal_font)

        y_pos = 200

        # Print receipt details
        receipt_data = data.get('receipt_data', {})

        # Date and time
        if 'date' in receipt_data:
            hdc.TextOut(100, y_pos, f"Date: {receipt_data['date']}")
            y_pos += 60

        # Receipt number
        if 'receipt_number' in receipt_data:
            hdc.TextOut(100, y_pos, f"Receipt #: {receipt_data['receipt_number']}")
            y_pos += 60

        # Customer info
        if 'customer_name' in receipt_data:
            hdc.TextOut(100, y_pos, f"Customer: {receipt_data['customer_name']}")
            y_pos += 60

        y_pos += 40  # Space

        # Items
        if 'items' in receipt_data:
            hdc.TextOut(100, y_pos, "Items:")
            y_pos += 60

            for item in receipt_data['items']:
                item_name = item.get('name', 'Unknown')
                quantity = item.get('quantity', 1)
                price = item.get('price', 0)
                total = quantity * price

                hdc.TextOut(120, y_pos, f"{item_name}")
                y_pos += 50
                hdc.TextOut(140, y_pos, f"Qty: {quantity} x ${price:.2f} = ${total:.2f}")
                y_pos += 60

        y_pos += 40  # Space

        # Total
        if 'total' in receipt_data:
            bold_font = win32ui.CreateFont({
                "name": "Arial",
                "height": 50,
                "weight": 700,
            })
            hdc.SelectObject(bold_font)
            hdc.TextOut(100, y_pos, f"TOTAL: ${receipt_data['total']:.2f}")
            y_pos += 80

        # Footer
        if 'footer' in receipt_data:
            hdc.SelectObject(normal_font)
            hdc.TextOut(100, y_pos, receipt_data['footer'])

    def _print_reservation(self, hdc, data, page_width, page_height):
        """Print a reservation confirmation"""
        # Header
        header_font = win32ui.CreateFont({
            "name": "Arial",
            "height": 60,
            "weight": 700,
        })
        hdc.SelectObject(header_font)
        hdc.TextOut(100, 100, "RESERVATION CONFIRMATION")

        # Normal font for content
        normal_font = win32ui.CreateFont({
            "name": "Arial",
            "height": 40,
            "weight": 400,
        })
        hdc.SelectObject(normal_font)

        y_pos = 200

        # Print reservation details
        reservation_data = data.get('reservation_data', {})

        fields = [
            ('confirmation_number', 'Confirmation #'),
            ('customer_name', 'Name'),
            ('date', 'Date'),
            ('time', 'Time'),
            ('party_size', 'Party Size'),
            ('table_number', 'Table'),
            ('special_requests', 'Special Requests'),
            ('phone', 'Phone'),
            ('email', 'Email')
        ]

        for field_key, field_label in fields:
            if field_key in reservation_data:
                hdc.TextOut(100, y_pos, f"{field_label}: {reservation_data[field_key]}")
                y_pos += 60

    def print_receipt(self, pos_data):
        """Convenience method to print a POS receipt"""
        print_data = {
            'type': 'receipt',
            'document_name': f"Receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'receipt_data': pos_data
        }
        return self.print_document(print_data)

    def print_reservation(self, reservation_data):
        """Convenience method to print a reservation"""
        print_data = {
            'type': 'reservation',
            'document_name': f"Reservation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'reservation_data': reservation_data
        }
        return self.print_document(print_data)

    def _convert_html_to_pdf(self, html_content):
        """Convert HTML to PDF using the configured converter"""
        # Reload config from .env to get latest settings
        from dotenv import load_dotenv
        load_dotenv(override=True)

        # Get the selected PDF converter from config (reload from environment)
        pdf_converter = os.environ.get('PDF_CONVERTER', 'reportlab').lower()
        logger.info(f"Using PDF converter: {pdf_converter}")

        # Route to the appropriate converter based on configuration
        if pdf_converter == 'wkhtmltopdf':
            try:
                logger.info("🔧 Attempting wkhtmltopdf conversion...")
                result = self._convert_html_to_pdf_wkhtmltopdf(html_content)
                logger.info(f"✅ wkhtmltopdf conversion successful: {result}")
                return result
            except Exception as e:
                import traceback
                logger.warning(f"⚠️ wkhtmltopdf conversion failed: {type(e).__name__}: {str(e)}")
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                logger.info("🔄 Falling back to ReportLab renderer...")
                # Fall back to optimized receipt renderer
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')
                    tables = soup.find_all('table')
                    if tables:
                        logger.info("📊 Using optimized table-based receipt renderer")
                        return self._convert_receipt_html_to_pdf(html_content)
                except Exception as fallback_error:
                    logger.debug(f"Table-based renderer also failed: {fallback_error}")
                    pass
                logger.info("📄 Using basic ReportLab renderer")
                return self._convert_html_to_pdf_reportlab(html_content)

        elif pdf_converter == 'weasyprint':
            try:
                return self._convert_html_to_pdf_weasyprint(html_content)
            except Exception as e:
                logger.warning(f"WeasyPrint conversion failed: {e}, falling back to ReportLab")
                return self._convert_html_to_pdf_reportlab(html_content)

        elif pdf_converter == 'sumatrapdf':
            # SumatraPDF is actually a PDF printer/viewer, not a converter
            # So we'll use ReportLab for conversion and SumatraPDF for printing
            logger.info("Using ReportLab for conversion (SumatraPDF is for printing)")
            return self._convert_html_to_pdf_reportlab(html_content)

        else:  # Default to 'reportlab'
            # Try optimized receipt renderer for table-based receipts
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Check if this is a table-based receipt (most common format)
                tables = soup.find_all('table')
                if tables:
                    logger.info("Using optimized table-based receipt renderer")
                    return self._convert_receipt_html_to_pdf(html_content)
            except Exception as e:
                logger.warning(f"Could not use optimized renderer: {e}")

            # Fall back to general ReportLab renderer
            try:
                return self._convert_html_to_pdf_reportlab(html_content)
            except Exception as e:
                logger.error(f"Error converting HTML to PDF with ReportLab: {str(e)}")
                # Fall back to WeasyPrint if available
                return self._convert_html_to_pdf_weasyprint(html_content)

    def _convert_receipt_html_to_pdf(self, html_content):
        """Optimized HTML to PDF converter for table-based receipts with CSS parsing"""
        try:
            from reportlab.lib.units import mm
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import portrait
            from bs4 import BeautifulSoup
            import re

            # Create temp PDF file
            pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(pdf_fd)

            soup = BeautifulSoup(html_content, 'html.parser')

            # Detect if this is "urdhri punes" (work order) by checking title
            is_urdhri_punes = False
            title_element = soup.find('td', class_='title1') or soup.find('h1')
            if title_element:
                title_text = title_element.get_text().strip().lower()
                if 'urdhri' in title_text or 'punes' in title_text:
                    is_urdhri_punes = True
                    logger.info("Detected 'urdhri punes' - will add lines around column headers")

            # Parse CSS into a simple dictionary
            css_styles = {}
            for style_tag in soup.find_all('style'):
                css_text = style_tag.string or ''

                # Parse .classname { rules }
                for match in re.finditer(r'\.([a-zA-Z0-9_-]+)\s*\{([^}]+)\}', css_text):
                    class_name = match.group(1)
                    rules_text = match.group(2)
                    css_styles[class_name] = {}

                    for rule in rules_text.split(';'):
                        if ':' in rule:
                            prop, val = rule.split(':', 1)
                            prop = prop.strip()
                            val = val.replace('!important', '').strip()
                            css_styles[class_name][prop] = val

                # Parse tag selectors like tfoot, thead, hr, td, th, etc.
                for match in re.finditer(r'\b([a-z]+)\s*\{([^}]+)\}', css_text):
                    tag_name = match.group(1)
                    rules_text = match.group(2)

                    # Skip if already parsed as class or if it's a CSS keyword
                    if tag_name in ['html', 'body', 'import', 'media', 'font']:
                        continue

                    css_styles[tag_name] = {}
                    for rule in rules_text.split(';'):
                        if ':' in rule:
                            prop, val = rule.split(':', 1)
                            prop = prop.strip()
                            val = val.replace('!important', '').strip()
                            css_styles[tag_name][prop] = val

            # Override font sizes for specific classes to make them smaller
            font_size_overrides = {
                'title1': '14px',          # Fature Tatimore - smaller
                'title1_urdhri': '14px',   # Urdhri titles - smaller
                'tds-footer': '11px',      # Company, NIPT, Address - smaller
            }

            for class_name, size in font_size_overrides.items():
                if class_name in css_styles:
                    css_styles[class_name]['font-size'] = size

            logger.info(f"Parsed {len(css_styles)} CSS rules (classes + tags)")
            # Log some key CSS rules for debugging
            for key in ['title1', 'tds-footer', 'columnsSkontrino', 'columnsPershkrim', 'columnsTotal', 'tfoot', 'center-text']:
                if key in css_styles:
                    logger.info(f"  CSS '{key}': {css_styles[key]}")

            # Helper to get CSS value
            def get_css_value(element, css_prop, default):
                """Get CSS property value from element classes, inline styles, and parent tags"""
                # Priority: inline style > element classes > element tag > parent tag

                # 1. Check inline styles first (highest priority)
                inline_style = element.get('style', '')
                if inline_style and css_prop in inline_style:
                    # Simple parsing for inline styles
                    for style_part in inline_style.split(';'):
                        if ':' in style_part:
                            prop, val = style_part.split(':', 1)
                            if prop.strip() == css_prop:
                                return val.strip()

                # 2. Check element's own classes (reverse order for last-defined wins)
                classes = element.get('class', [])
                for cls in reversed(classes):
                    if cls in css_styles and css_prop in css_styles[cls]:
                        return css_styles[cls][css_prop]

                # 3. Check element's own tag
                if element.name in css_styles and css_prop in css_styles[element.name]:
                    return css_styles[element.name][css_prop]

                # 4. Check parent elements (tfoot, thead, tbody, etc.)
                parent = element.parent
                while parent:
                    if parent.name in css_styles and css_prop in css_styles[parent.name]:
                        return css_styles[parent.name][css_prop]
                    parent = parent.parent
                    # Only check up to 2 levels to avoid over-inheritance
                    if parent and parent.name == 'table':
                        break

                return default

            # Setup PDF
            width = 80 * mm
            height = 297 * mm
            c = canvas.Canvas(pdf_path, pagesize=portrait((width, height)))

            y = height - 5 * mm  # Smaller top margin
            margin = 3 * mm  # Smaller side margins

            # Font size scaling factor from config - reload from environment
            from dotenv import load_dotenv
            load_dotenv(override=True)  # Reload .env to get latest FONT_SCALE
            try:
                font_scale = float(os.environ.get('FONT_SCALE', '0.8'))
            except:
                font_scale = 0.8

            logger.info(f"Using font scale: {font_scale} ({int(font_scale * 100)}%)")

            def draw_text(text, y_pos, font_size=9, bold=False, align='left'):
                """Draw text with alignment"""
                # Apply font scaling
                scaled_font_size = max(6, int(font_size * font_scale))  # Minimum 6pt

                font = "Helvetica-Bold" if bold else "Helvetica"
                c.setFont(font, scaled_font_size)

                if align == 'center':
                    c.drawCentredString(width / 2, y_pos, text)
                elif align == 'right':
                    c.drawRightString(width - margin, y_pos, text)
                else:
                    c.drawString(margin, y_pos, text)

                return scaled_font_size * 0.35  # Return line height in mm (tighter spacing)

            def draw_solid_line(y_pos, line_width=0.5):
                """Draw a solid separator line"""
                c.setLineWidth(line_width)
                c.line(margin, y_pos, width - margin, y_pos)
                c.setLineWidth(1)  # Reset line width

            def draw_qr_code(data, y_pos, qr_size=30):
                """Generate and draw QR code"""
                try:
                    import qrcode
                    from reportlab.lib.utils import ImageReader

                    # Generate QR code
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=1,
                    )
                    qr.add_data(data)
                    qr.make(fit=True)

                    # Create image
                    img = qr.make_image(fill_color="black", back_color="white")

                    # Save to temp file
                    qr_fd, qr_path = tempfile.mkstemp(suffix='.png')
                    os.close(qr_fd)
                    img.save(qr_path)

                    # Draw QR code centered
                    qr_x = (width - qr_size * mm) / 2
                    c.drawImage(qr_path, qr_x, y_pos - qr_size * mm,
                               width=qr_size * mm, height=qr_size * mm)

                    # Clean up temp file
                    try:
                        os.unlink(qr_path)
                    except:
                        pass

                    return qr_size  # Return height used in mm
                except Exception as e:
                    logger.warning(f"Could not generate QR code: {e}")
                    return 0

            # Track sections to add solid lines at correct positions
            last_section = None  # Track what we just processed

            # Process all tables
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    # Check if this row is in tfoot or tbody
                    is_footer_row = row.find_parent('tfoot') is not None
                    is_tbody_row = row.find_parent('tbody') is not None

                    cells = row.find_all(['td', 'th'])

                    if not cells:
                        continue

                    # Check if this row ONLY contains a line (hr or div with dashed-line/div_line)
                    # If cell only contains these elements with no other text, it's a separator row
                    is_line_only_row = False
                    for cell in cells:
                        cell_text = cell.get_text().strip()
                        has_line_div = cell.find('div', class_=['div_line', 'dashed-line'])
                        has_hr = cell.find('hr')

                        if (has_line_div or has_hr) and not cell_text:
                            is_line_only_row = True
                            break

                    if is_line_only_row:
                        # Remove all HTML dashed lines - we'll add solid lines strategically
                        continue

                    # Single cell (title, info, etc.)
                    if len(cells) == 1 or (len(cells) == 2 and cells[0].get('colspan')):
                        cell = cells[0]

                        # Check if this cell contains SVG (QR code)
                        svg_element = cell.find('svg')
                        if svg_element:
                            # Extract QR code data from nearby elements
                            # Look for NIVF or NSLF in previous rows
                            qr_data = ""
                            for prev_row in table.find_all('tr'):
                                prev_text = prev_row.get_text()
                                if 'NIVF:' in prev_text or 'NSLF:' in prev_text:
                                    # Extract the hash/code after the colon
                                    parts = prev_text.split(':', 1)
                                    if len(parts) > 1:
                                        qr_data = parts[1].strip()
                                        break

                            if qr_data:
                                y -= 3 * mm  # Space before QR
                                qr_height = draw_qr_code(qr_data, y, qr_size=30)
                                y -= (qr_height + 3) * mm  # Space after QR
                            continue

                        text = cell.get_text().strip()

                        if not text:
                            continue

                        # Get CSS styling from the cell
                        font_size_str = get_css_value(cell, 'font-size', '9px').replace('px', '').replace('pt', '')
                        try:
                            font_size = int(float(font_size_str))
                        except:
                            font_size = 9

                        # Apply font scaling
                        font_size = max(6, int(font_size * font_scale))

                        weight = get_css_value(cell, 'font-weight', 'normal')
                        bold = weight in ['bold', '500', '600', '700', '800', '900']

                        align_val = get_css_value(cell, 'text-align', 'left')

                        # Footer rows should be centered (tfoot has text-align: center)
                        if is_footer_row:
                            align_val = 'center'
                            # Add line before footer (if not QR code or NSLF/NIVF)
                            if 'Gjeneruar' in text or 'Generated' in text:
                                if last_section != 'footer_line_added':
                                    y -= 2 * mm
                                    draw_solid_line(y)
                                    y -= 3 * mm
                                    last_section = 'footer_line_added'

                        # Check if contains h1/h2 (makes it bold automatically and larger)
                        heading = cell.find(['h1', 'h2'])
                        if heading:
                            bold = True
                            # h1 should be larger - but respect CSS if it's already set larger
                            if heading.name == 'h1' and font_size < 12:
                                font_size = 12
                            elif heading.name == 'h2' and font_size < 10:
                                font_size = 10

                        # Check for <br> tags and split text into multiple lines
                        if cell.find('br'):
                            # Handle line breaks in text (like NSLF field)
                            text_parts = []
                            for content in cell.stripped_strings:
                                text_parts.append(content)

                            # Print each part on its own line
                            for part in text_parts:
                                line_height = draw_text(part, y, font_size, bold, align_val)
                                y -= (line_height + 1.5) * mm
                        else:
                            # Check if this is end of company header section (tds-footer class)
                            cell_classes = cell.get('class', [])
                            if 'tds-footer' in cell_classes:
                                last_section = 'company_header'
                            # Check if this is operator/tavolina/data info (columnsSkontrino)
                            elif 'columnsSkontrino' in cell_classes and last_section == 'company_header':
                                # Add solid line BEFORE the receipt info section (Data, Operator, etc)
                                y -= 2 * mm
                                draw_solid_line(y)
                                y -= 3 * mm
                                last_section = 'receipt_info'

                            # Regular single-line text
                            line_height = draw_text(text, y, font_size, bold, align_val)

                            # Tighter spacing for more compact layout
                            if font_size >= 14:
                                spacing = 1.5
                            elif font_size >= 12:
                                spacing = 1.2
                            else:
                                spacing = 0.8
                            y -= (line_height + spacing) * mm

                            # Check if this is "Tavolina" or "Menyra e Pageses" field - add line AFTER
                            # This check must be AFTER drawing text and spacing
                            if 'Tavolina:' in text or 'Menyra e Pageses:' in text:
                                # Add spacing and solid line AFTER Tavolina/Menyra e Pageses
                                y -= 1 * mm  # Extra space before line
                                draw_solid_line(y)
                                y -= 2 * mm  # Space after line
                                last_section = 'after_tavolina'

                    # Multi-cell row (table data)
                    elif len(cells) >= 2:
                        # Filter out empty cells
                        non_empty_cells = [cell for cell in cells if cell.get_text().strip()]

                        if not non_empty_cells:
                            continue

                        # Extract cell texts from non-empty cells
                        cell_texts = [cell.get_text().strip() for cell in non_empty_cells]

                        # Check if this is a header row (contains <th> tags)
                        is_header = any(cell.name == 'th' for cell in non_empty_cells)

                        # Get styling from first non-empty cell
                        first_cell = non_empty_cells[0]
                        font_size_str = get_css_value(first_cell, 'font-size', '9px').replace('px', '').replace('pt', '')
                        try:
                            font_size = int(float(font_size_str))
                        except:
                            font_size = 10 if is_header else 9

                        # Apply font scaling
                        font_size = max(6, int(font_size * font_scale))

                        weight = get_css_value(first_cell, 'font-weight', 'normal')
                        bold = weight in ['bold', '500', '600', '700', '800', '900'] or is_header

                        # Check if any cell contains h1/h2 (for TOTALI row)
                        has_heading = any(cell.find(['h1', 'h2']) for cell in non_empty_cells)
                        if has_heading:
                            bold = True
                            if font_size < 12:
                                font_size = 12

                        # Get text alignment from cells
                        alignments = [get_css_value(cell, 'text-align', 'left') for cell in non_empty_cells]

                        # Format based on number of non-empty columns
                        if len(non_empty_cells) == 2:
                            # Two columns: Could be TOTALI row OR Sasia/Artikull (Fature Porosi)
                            left_text = cell_texts[0]
                            right_text = cell_texts[1]

                            # Check if this is TOTALI row (has heading)
                            if has_heading:
                                # Add solid line before TOTALI
                                y -= 2 * mm
                                draw_solid_line(y)
                                y -= 3 * mm
                                last_section = 'totali'

                            # Check if this is a Fature Porosi table (Sasia + Artikull)
                            # Detect by checking if left text contains "x" (quantity marker)
                            is_fature_porosi = 'x' in left_text.lower() and not has_heading

                            if is_fature_porosi and is_tbody_row:
                                # Fature Porosi: Two columns with Sasia (left) and Artikull (right)
                                # Need word wrapping for long Artikull names
                                font_name = "Helvetica-Bold" if bold else "Helvetica"
                                c.setFont(font_name, font_size)

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
                                    # Need to wrap - split into words
                                    words = right_text.split()
                                    lines = []
                                    current_line = ""

                                    for word in words:
                                        test_line = current_line + " " + word if current_line else word
                                        test_width = c.stringWidth(test_line, font_name, font_size)

                                        if test_width <= (artikull_width - 2*mm):
                                            current_line = test_line
                                        else:
                                            if current_line:
                                                lines.append(current_line)
                                            current_line = word

                                    if current_line:
                                        lines.append(current_line)

                                    # Draw first line
                                    if lines:
                                        c.drawString(artikull_x, y, lines[0])

                                        # Draw remaining lines (indented under Artikull column)
                                        for additional_line in lines[1:]:
                                            y -= (font_size * 0.35 + 0.8) * mm
                                            c.drawString(artikull_x, y, additional_line)

                                # Add extra spacing after Fature Porosi product row
                                y -= 2 * mm  # Extra spacing between products
                            else:
                                # Regular 2-column format (TOTALI, etc.)
                                # Check alignment of right cell
                                if alignments[1] == 'center':
                                    # Draw left text on left, right text centered on right side
                                    c.setFont("Helvetica-Bold" if bold else "Helvetica", font_size)
                                    c.drawString(margin, y, left_text)
                                    c.drawCentredString(width - margin - 15*mm, y, right_text)
                                elif alignments[1] == 'right':
                                    # Traditional left-right alignment
                                    line = f"{left_text:<35} {right_text:>10}"
                                    c.setFont("Helvetica-Bold" if bold else "Helvetica", font_size)
                                    c.drawString(margin, y, line)
                                else:
                                    # Both left-aligned with spacing
                                    line = f"{left_text:<25} {right_text}"
                                    c.setFont("Helvetica-Bold" if bold else "Helvetica", font_size)
                                    c.drawString(margin, y, line)
                        elif len(non_empty_cells) == 4:
                            # Four columns: Artikull, Sasia, Cmimi, Vlera
                            c.setFont("Helvetica-Bold" if (bold or is_header) else "Helvetica", font_size)

                            # Define column widths to match alignment
                            col_width = (width - 2 * margin) / 4

                            if is_header:
                                # Draw solid line before header (for ALL receipts)
                                y -= 1 * mm  # Small space before line
                                draw_solid_line(y)
                                y -= 3 * mm  # More space after line, before text

                                # Header row - centered in each column
                                for i, text in enumerate(cell_texts):
                                    x_pos = margin + (i * col_width) + (col_width / 2)
                                    c.drawCentredString(x_pos, y, text)

                                # Draw solid line after header (for ALL receipts)
                                y -= 3 * mm  # More space before line, after text
                                draw_solid_line(y)
                                y -= 1 * mm  # Small space after line

                                last_section = 'table_header'
                            else:
                                # Data row - align to match header columns
                                # Artikull (left), Sasia (center), Cmimi (center), Vlera (center)

                                # Handle first column (Artikull) with word wrapping if needed
                                artikull_text = cell_texts[0]
                                x_pos_artikull = margin

                                # Calculate max width for Artikull column (leave space for other columns)
                                max_artikull_width = col_width - 2*mm  # Add small padding

                                # Check if text fits in one line
                                font_name = "Helvetica-Bold" if (bold or is_header) else "Helvetica"
                                text_width = c.stringWidth(artikull_text, font_name, font_size)

                                if text_width <= max_artikull_width:
                                    # Fits in one line - draw normally
                                    c.drawString(x_pos_artikull, y, artikull_text)

                                    # Draw other columns on same line
                                    for i in range(1, len(cell_texts)):
                                        text = cell_texts[i]
                                        x_pos = margin + (i * col_width)
                                        x_center = x_pos + (col_width / 2)
                                        c.drawCentredString(x_center, y, text)
                                else:
                                    # Text too long - need to wrap
                                    # Split into words and wrap
                                    words = artikull_text.split()
                                    lines = []
                                    current_line = ""

                                    for word in words:
                                        test_line = current_line + " " + word if current_line else word
                                        test_width = c.stringWidth(test_line, font_name, font_size)

                                        if test_width <= max_artikull_width:
                                            current_line = test_line
                                        else:
                                            if current_line:
                                                lines.append(current_line)
                                            current_line = word

                                    if current_line:
                                        lines.append(current_line)

                                    # Draw first line with other columns
                                    if lines:
                                        c.drawString(x_pos_artikull, y, lines[0])

                                        # Draw other columns on first line
                                        for i in range(1, len(cell_texts)):
                                            text = cell_texts[i]
                                            x_pos = margin + (i * col_width)
                                            x_center = x_pos + (col_width / 2)
                                            c.drawCentredString(x_center, y, text)

                                        # Draw remaining lines of Artikull text (if any)
                                        for additional_line in lines[1:]:
                                            y -= (font_size * 0.35 + 0.8) * mm
                                            c.drawString(x_pos_artikull, y, additional_line)

                                # Add extra spacing after product row if in tbody
                                if is_tbody_row:
                                    y -= 2 * mm  # Extra spacing between products (green arrows in image)
                        else:
                            # Check if this is a tax summary table row (contains TVSH or Tipi keywords)
                            is_tax_table_row = any('TVSH' in text or 'Tipi' in text for text in cell_texts)

                            # Also check if we're currently inside a tax table (last_section is tax_table_header)
                            # This handles data rows that don't contain the keywords
                            is_inside_tax_table = last_section == 'tax_table_header'

                            if is_tax_table_row or is_inside_tax_table:
                                # Skip if we've already rendered the complete tax table
                                if last_section == 'tax_table_complete':
                                    continue

                                # Check if this is header row (must contain both Tipi AND TVSH)
                                is_tax_header = 'Tipi' in cell_texts and 'TVSH' in cell_texts

                                if is_tax_header:
                                    # Skip if we've already rendered the header
                                    if last_section == 'tax_table_header' or last_section == 'tax_table_complete':
                                        continue

                                    # Add line before tax table
                                    y -= 2 * mm
                                    draw_solid_line(y)
                                    y -= 3 * mm

                                    # Use readable font for tax table (9pt for better readability)
                                    tax_font_size = 9

                                    # Calculate column widths for tax table (4 columns)
                                    num_cols = len(cell_texts)
                                    tax_col_width = (width - 2 * margin) / num_cols

                                    # Row height (increased for larger font)
                                    row_height = 5.5 * mm

                                    # Draw header row with borders
                                    c.setFont("Helvetica-Bold", tax_font_size)
                                    for i, text in enumerate(cell_texts):
                                        x_pos = margin + (i * tax_col_width)
                                        # Draw cell border
                                        c.setLineWidth(0.3)
                                        c.rect(x_pos, y - row_height,
                                              tax_col_width, row_height,
                                              stroke=1, fill=0)
                                        # Draw text centered in cell (vertically and horizontally)
                                        x_center = x_pos + (tax_col_width / 2)
                                        y_center = y - (row_height / 2) + (tax_font_size * 0.3)
                                        c.drawCentredString(x_center, y_center, text)

                                    y -= row_height
                                    last_section = 'tax_table_header'
                                    continue

                                elif is_inside_tax_table:
                                    # Tax data row (we're inside tax table from header)
                                    # Use readable font for tax table data
                                    tax_font_size = 9

                                    # Calculate column widths
                                    num_cols = len(cell_texts)
                                    tax_col_width = (width - 2 * margin) / num_cols

                                    # Row height (increased for larger font)
                                    row_height = 5.5 * mm

                                    # Draw data row with borders
                                    c.setFont("Helvetica", tax_font_size)
                                    for i, text in enumerate(cell_texts):
                                        x_pos = margin + (i * tax_col_width)
                                        # Draw cell border
                                        c.setLineWidth(0.3)
                                        c.rect(x_pos, y - row_height,
                                              tax_col_width, row_height,
                                              stroke=1, fill=0)
                                        # Draw text centered in cell
                                        x_center = x_pos + (tax_col_width / 2)
                                        y_center = y - (row_height / 2) + (tax_font_size * 0.3)
                                        c.drawCentredString(x_center, y_center, text)

                                    y -= row_height

                                    # Add line after tax table and mark as complete
                                    y -= 1 * mm
                                    draw_solid_line(y)
                                    y -= 2 * mm
                                    last_section = 'tax_table_complete'
                                    continue
                            else:
                                # General: space-separated
                                line = "  ".join(cell_texts)
                                c.setFont("Helvetica-Bold" if bold else "Helvetica", font_size)
                                c.drawString(margin, y, line)

                        # Tighter spacing for compact layout
                        spacing = 1.5 if font_size >= 14 else (1.2 if font_size >= 12 else 0.8)
                        y -= (font_size * 0.35 + spacing) * mm

                    # Check for page break
                    if y < 20 * mm:
                        c.showPage()
                        y = height - 10 * mm

            c.save()
            logger.info(f"Receipt PDF created successfully: {pdf_path}")
            return pdf_path

        except Exception as e:
            logger.error(f"Error in optimized receipt renderer: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def _convert_html_to_pdf_wkhtmltopdf(self, html_content):
        """Convert HTML to PDF using wkhtmltopdf (best CSS support)"""
        try:
            import pdfkit

            # Try to find wkhtmltopdf executable
            # First check if running as PyInstaller bundle
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                bundle_dir = os.path.dirname(sys.executable)
                # PyInstaller extracts to _MEIPASS temporary folder
                if hasattr(sys, '_MEIPASS'):
                    meipass_dir = sys._MEIPASS
                    logger.info(f"📦 Running as PyInstaller bundle")
                    logger.info(f"   Executable dir: {bundle_dir}")
                    logger.info(f"   Temp extract dir: {meipass_dir}")
                else:
                    meipass_dir = bundle_dir
                    logger.info(f"📦 Running as compiled executable (no _MEIPASS)")
            else:
                # Running as script
                bundle_dir = os.path.dirname(os.path.abspath(__file__))
                meipass_dir = bundle_dir
                logger.info(f"🐍 Running as Python script from: {bundle_dir}")

            wkhtmltopdf_paths = [
                # Check in PyInstaller temp directory (where bundled files are extracted)
                os.path.join(meipass_dir, "wkhtmltopdf.exe") if hasattr(sys, '_MEIPASS') else None,
                # Check in the same directory as the executable (for bundled version)
                os.path.join(bundle_dir, "wkhtmltopdf.exe"),
                # Check in standard installation paths
                r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
                r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
                # Check in script directory (for development)
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "wkhtmltopdf.exe"),
            ]

            # Remove None values
            wkhtmltopdf_paths = [p for p in wkhtmltopdf_paths if p is not None]

            wkhtmltopdf_path = None
            logger.info(f"🔍 Searching for wkhtmltopdf.exe in {len(wkhtmltopdf_paths)} locations...")
            for path in wkhtmltopdf_paths:
                logger.info(f"   Checking: {path}")
                if os.path.exists(path):
                    wkhtmltopdf_path = path
                    logger.info(f"✅ Found wkhtmltopdf at: {path}")
                    break
                else:
                    logger.info(f"   ❌ Not found")

            if not wkhtmltopdf_path:
                logger.error("❌ wkhtmltopdf.exe not found in any location!")
                logger.error(f"   Searched locations: {wkhtmltopdf_paths}")
                logger.error("   Falling back to ReportLab renderer...")
                raise Exception("wkhtmltopdf not installed")

            # Inject CSS to make title, company name, and address smaller
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Add CSS to adjust font sizes and improve text rendering
            style_tag = soup.new_tag('style')
            style_tag.string = """
                /* Improve text rendering for better readability */
                * {
                    -webkit-font-smoothing: antialiased !important;
                    -moz-osx-font-smoothing: grayscale !important;
                    text-rendering: optimizeLegibility !important;
                }

                /* Center the "Fature" title */
                h1 {
                    text-align: center !important;
                    font-size: 18px !important;
                    margin: 5px 0 !important;
                    font-weight: bold !important;
                }

                .title1 h1 {
                    font-size: 18px !important;
                    margin: 5px 0 !important;
                    text-align: center !important;
                }

                .tds-footer {
                    font-size: 14px !important;
                }

                /* Increase Artikull column font size for Full Invoice (4-column table) */
                .columnsPershkrim {
                    font-size: 14px !important;
                    font-weight: 600 !important;
                }

                /* Increase Artikull column font size for Fature Porosi (2-column table) */
                .columnsPershkrim_urdhri {
                    font-size: 15px !important;
                    font-weight: 600 !important;
                }

                /* Improve overall text clarity */
                body, td, th, p, span, div {
                    -webkit-font-smoothing: antialiased !important;
                    -moz-osx-font-smoothing: grayscale !important;
                }
            """

            if soup.head:
                soup.head.append(style_tag)
            else:
                head = soup.new_tag('head')
                head.append(style_tag)
                if soup.html:
                    soup.html.insert(0, head)

            modified_html = str(soup)

            # Create temp HTML file with modified CSS
            html_fd, html_path = tempfile.mkstemp(suffix='.html')
            with os.fdopen(html_fd, 'w', encoding='utf-8') as f:
                f.write(modified_html)

            # Create temp PDF file
            pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(pdf_fd)

            # Configure wkhtmltopdf
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

            # Same options as print_server/app.py
            options = {
                'page-width': '80mm',
                'page-height': '297mm',
                'margin-top': '0mm',
                'margin-bottom': '0mm',
                'margin-left': '0mm',
                'margin-right': '0mm',
                'zoom': 1,
                'disable-smart-shrinking': '',
            }

            # Convert HTML to PDF
            pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)

            # Clean up temp HTML file
            try:
                os.unlink(html_path)
            except:
                pass

            logger.info(f"HTML converted to PDF with wkhtmltopdf: {pdf_path}")
            return pdf_path

        except ImportError:
            # pdfkit not installed - silently raise to trigger fallback
            raise Exception("pdfkit library not installed")
        except Exception as e:
            # Any error (missing executable, conversion failure) - silently raise to trigger fallback
            raise

    def _convert_html_to_pdf_weasyprint(self, html_content):
        """Convert HTML to PDF using WeasyPrint (requires GTK on Windows)"""
        try:
            from weasyprint import HTML, CSS

            # Create a temporary file for the PDF
            pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(pdf_fd)

            # Add custom CSS for better receipt printing
            custom_css = CSS(string='''
                @page {
                    size: 80mm auto;
                    margin: 0;
                    padding: 0;
                }
                body {
                    margin: 0;
                    padding: 5mm;
                    font-family: Arial, sans-serif;
                }
            ''')

            # Convert HTML to PDF
            HTML(string=html_content).write_pdf(pdf_path, stylesheets=[custom_css])

            logger.info(f"HTML converted to PDF with WeasyPrint: {pdf_path}")
            return pdf_path

        except Exception as e:
            logger.error(f"Error converting HTML to PDF with WeasyPrint: {str(e)}")
            raise

    def _convert_html_to_pdf_reportlab(self, html_content):
        """Convert HTML to PDF using reportlab and BeautifulSoup"""
        try:
            from reportlab.lib.units import mm
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import portrait
            from bs4 import BeautifulSoup
            import re

            # Create a temporary file for the PDF
            pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(pdf_fd)

            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract CSS styles from <style> tags with improved parser
            css_rules = {}
            for style_tag in soup.find_all('style'):
                css_text = style_tag.string
                if css_text:
                    # Remove comments
                    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)

                    # Match CSS rules: selector { properties }
                    # This handles both .class and tag selectors
                    pattern = r'([\.#]?[a-zA-Z0-9_-]+(?:\s+[a-zA-Z0-9_-]+)*)\s*\{([^}]+)\}'
                    matches = re.findall(pattern, css_text, re.MULTILINE)

                    for selector, rules in matches:
                        selector = selector.strip()

                        # Extract class name (remove the dot)
                        if selector.startswith('.'):
                            rule_name = selector[1:]
                        else:
                            rule_name = selector

                        # Skip complex selectors for now
                        if ' ' in rule_name or '>' in rule_name or '+' in rule_name:
                            continue

                        css_rules[rule_name] = {}

                        # Parse individual properties
                        for rule in rules.split(';'):
                            if ':' in rule:
                                prop, value = rule.split(':', 1)
                                prop = prop.strip()
                                value = value.strip().replace('!important', '').strip()
                                css_rules[rule_name][prop] = value

            # Debug: Log parsed CSS rules
            logger.info(f"Parsed {len(css_rules)} CSS rules")
            for rule_name in list(css_rules.keys())[:5]:  # Log first 5
                logger.info(f"  CSS rule '{rule_name}': {css_rules[rule_name]}")

            def get_style(element, inherit_from_parent=True):
                """Get computed style for an element, inheriting from parent"""
                style = {
                    'font-size': 9,
                    'font-weight': 'normal',
                    'text-align': 'left',
                    'bold': False
                }

                element_classes = element.get('class', [])
                logger.debug(f"Getting style for {element.name} with classes: {element_classes}")

                # Inherit styles from parent elements if requested
                if inherit_from_parent and element.parent:
                    parent = element.parent
                    # Check parent's classes for inherited styles
                    parent_classes = parent.get('class', [])
                    for class_name in parent_classes:
                        if class_name in css_rules:
                            parent_css = css_rules[class_name]
                            if 'font-size' in parent_css:
                                size_str = parent_css['font-size'].replace('px', '').replace('!important', '').strip()
                                try:
                                    style['font-size'] = int(float(size_str))
                                except:
                                    pass
                            if 'font-weight' in parent_css:
                                weight = parent_css['font-weight'].replace('!important', '').strip()
                                if weight in ['bold', '500', '600', '700', '800', '900']:
                                    style['bold'] = True
                            if 'text-align' in parent_css:
                                align = parent_css['text-align'].replace('!important', '').strip()
                                style['text-align'] = align

                # Apply tag-level CSS
                if element.name in css_rules:
                    tag_css = css_rules[element.name]
                    if 'font-size' in tag_css:
                        size_str = tag_css['font-size'].replace('px', '').replace('!important', '').strip()
                        try:
                            style['font-size'] = int(float(size_str))
                        except:
                            pass
                    if 'font-weight' in tag_css:
                        weight = tag_css['font-weight'].replace('!important', '').strip()
                        if weight in ['bold', '600', '700', '800', '900']:
                            style['bold'] = True
                    if 'text-align' in tag_css:
                        align = tag_css['text-align'].replace('!important', '').strip()
                        style['text-align'] = align

                # Apply class-level CSS (overrides tag and parent styles)
                classes = element.get('class', [])
                for class_name in classes:
                    if class_name in css_rules:
                        class_css = css_rules[class_name]
                        if 'font-size' in class_css:
                            size_str = class_css['font-size'].replace('px', '').replace('!important', '').strip()
                            try:
                                style['font-size'] = int(float(size_str))
                            except:
                                pass
                        if 'font-weight' in class_css:
                            weight = class_css['font-weight'].replace('!important', '').strip()
                            if weight in ['bold', '500', '600', '700', '800', '900']:
                                style['bold'] = True
                        if 'text-align' in class_css:
                            align = class_css['text-align'].replace('!important', '').strip()
                            style['text-align'] = align

                # Check inline styles (highest priority)
                inline_style = element.get('style', '')
                if inline_style:
                    if 'bold' in inline_style or 'font-weight' in inline_style:
                        style['bold'] = True
                    if 'text-align' in inline_style:
                        if 'center' in inline_style:
                            style['text-align'] = 'center'
                        elif 'right' in inline_style:
                            style['text-align'] = 'right'
                    if 'font-size' in inline_style:
                        size_match = re.search(r'font-size:\s*(\d+)px', inline_style)
                        if size_match:
                            try:
                                style['font-size'] = int(size_match.group(1))
                            except:
                                pass

                return style

            # Create PDF with 80mm width (thermal printer size)
            width = 80 * mm
            height = 297 * mm  # A4 height, will auto-adjust
            margin_left = 5 * mm
            margin_right = 5 * mm
            usable_width = width - margin_left - margin_right

            c = canvas.Canvas(pdf_path, pagesize=portrait((width, height)))

            y_position = height - 10 * mm
            line_height = 4 * mm

            def add_text(text, font_size=9, align="left", bold=False):
                nonlocal y_position

                font_name = "Helvetica-Bold" if bold else "Helvetica"
                c.setFont(font_name, font_size)

                # Adjust line height based on font size
                current_line_height = max(line_height, font_size * 0.35)

                # Word wrap
                words = text.split()
                line = ""
                lines_to_print = []

                for word in words:
                    test_line = line + " " + word if line else word
                    if c.stringWidth(test_line, font_name, font_size) < usable_width:
                        line = test_line
                    else:
                        if line:
                            lines_to_print.append(line)
                        line = word

                if line:
                    lines_to_print.append(line)

                # Print each line
                for text_line in lines_to_print:
                    if y_position < 20 * mm:
                        c.showPage()
                        y_position = height - 10 * mm
                        c.setFont(font_name, font_size)

                    x_pos = margin_left
                    if align == "center":
                        text_width = c.stringWidth(text_line, font_name, font_size)
                        x_pos = (width - text_width) / 2
                    elif align == "right":
                        text_width = c.stringWidth(text_line, font_name, font_size)
                        x_pos = width - margin_right - text_width

                    c.drawString(x_pos, y_position, text_line)
                    y_position -= current_line_height

            def add_line(style="dashed"):
                nonlocal y_position
                y_position -= 2 * mm

                if y_position < 20 * mm:
                    c.showPage()
                    y_position = height - 10 * mm

                if style == "dashed":
                    c.setDash(3, 3)
                else:
                    c.setDash(1, 0)

                c.line(margin_left, y_position, width - margin_right, y_position)
                c.setDash(1, 0)  # Reset to solid
                y_position -= 3 * mm

            # Track processed elements to avoid duplicates
            processed_elements = set()

            # Process HTML elements (skip those inside tables - handled separately)
            for element in soup.find_all(['h1', 'h2', 'p', 'hr', 'div']):
                # Skip if inside a table (tables are handled separately)
                if element.find_parent('table'):
                    continue

                # Skip if already processed
                if id(element) in processed_elements:
                    continue

                # Get text and computed style
                text = element.get_text().strip()
                if not text and element.name != 'hr':
                    continue

                # Mark as processed
                processed_elements.add(id(element))

                style = get_style(element)

                # Handle different elements
                if element.name == 'h1':
                    # h1 typically larger and bold - inherit parent styles
                    size = style.get('font-size', 16)
                    add_text(text, font_size=size, align=style['text-align'], bold=True)
                    y_position -= 2 * mm
                elif element.name == 'h2':
                    # h2 medium size and bold
                    size = style.get('font-size', 14)
                    add_text(text, font_size=size, align=style['text-align'], bold=True)
                    y_position -= 2 * mm
                elif element.name == 'hr':
                    # Check if dashed
                    style_attr = element.get('style', '')
                    class_attr = element.get('class', [])
                    if 'dashed' in style_attr or any('dashed' in str(c) for c in class_attr):
                        add_line("dashed")
                    else:
                        add_line("solid")
                elif text:
                    # Use computed style
                    add_text(text, font_size=style['font-size'], align=style['text-align'], bold=style['bold'])

            # Handle tables with CSS styling
            for table in soup.find_all('table'):
                table_rows = []
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        # Store cell data with styles
                        cell_info = []
                        for cell in cells:
                            # Get the cell's own style
                            cell_style = get_style(cell, inherit_from_parent=False)

                            # Check if cell contains a heading (h1, h2) - inherit cell's classes
                            child_heading = cell.find(['h1', 'h2'])
                            if child_heading:
                                # Heading inherits from parent cell's classes
                                child_style = get_style(child_heading, inherit_from_parent=True)
                                cell_style = child_style

                            cell_info.append({
                                'text': cell.get_text().strip(),
                                'style': cell_style,
                                'is_th': cell.name == 'th',
                                'has_heading': child_heading is not None
                            })
                        table_rows.append(cell_info)

                # Print table rows with proper styling
                for row_cells in table_rows:
                    if len(row_cells) == 1:
                        # Single column (like title or single info line)
                        cell = row_cells[0]
                        font_size = cell['style']['font-size']

                        # Add extra spacing for headings
                        if cell['has_heading']:
                            y_position -= 1 * mm

                        add_text(
                            cell['text'],
                            font_size=font_size,
                            align=cell['style']['text-align'],
                            bold=cell['style']['bold'] or cell['is_th']
                        )

                        # Add extra spacing after headings
                        if cell['has_heading']:
                            y_position -= 1 * mm
                    elif len(row_cells) == 2:
                        # Two columns - formatted side by side
                        left_cell = row_cells[0]
                        right_cell = row_cells[1]

                        # Determine alignment based on styles
                        if right_cell['style']['text-align'] == 'right':
                            line = f"{left_cell['text']:<35} {right_cell['text']:>10}"
                        else:
                            line = f"{left_cell['text']:<25} {right_cell['text']:<20}"

                        # Use the larger font size and check if either is bold
                        font_size = max(left_cell['style']['font-size'], right_cell['style']['font-size'])
                        is_bold = left_cell['style']['bold'] or right_cell['style']['bold'] or left_cell['is_th'] or right_cell['is_th']

                        add_text(line, font_size=font_size, align="left", bold=is_bold)
                    elif len(row_cells) >= 3:
                        # Multiple columns
                        if len(row_cells) == 4:
                            # 4 columns (Artikull, Sasia, Cmimi, Vlera)
                            # Don't truncate Artikull - let it wrap naturally
                            # Format: Full Artikull text + aligned numeric columns
                            artikull_full = row_cells[0]['text']
                            sasia = row_cells[1]['text']
                            cmimi = row_cells[2]['text']
                            vlera = row_cells[3]['text']

                            # Build line with full Artikull text (no truncation)
                            # Only align the numeric columns
                            line = f"{artikull_full}  {sasia:>6} {cmimi:>8} {vlera:>8}"
                        else:
                            # General multi-column formatting
                            line = "  ".join([cell['text'] for cell in row_cells])

                        # Use max font size and check if any cell is bold
                        font_size = max([cell['style']['font-size'] for cell in row_cells])
                        is_bold = any(cell['style']['bold'] or cell['is_th'] for cell in row_cells)

                        add_text(line, font_size=font_size, align="left", bold=is_bold)

                y_position -= 2 * mm  # Space after table

            c.save()
            logger.info(f"HTML converted to PDF with ReportLab: {pdf_path}")
            return pdf_path

        except Exception as e:
            logger.error(f"Error converting HTML to PDF with ReportLab: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def _print_pdf_file(self, pdf_path, printer_name):
        """Print a PDF file using Windows printing"""
        try:
            # Method 1: Try using SumatraPDF (lightweight and good for silent printing)
            # Check if running as PyInstaller bundle
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                bundle_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                bundle_dir = os.path.dirname(os.path.abspath(__file__))

            sumatra_paths = [
                # Check in the same directory as the executable (for bundled version)
                os.path.join(bundle_dir, "SumatraPDF.exe"),
                # Check in standard installation paths
                r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
                r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
            ]

            logger.info("🔍 Searching for SumatraPDF.exe...")
            for sumatra_path in sumatra_paths:
                logger.debug(f"   Checking: {sumatra_path}")
                if os.path.exists(sumatra_path):
                    logger.info(f"✅ Found SumatraPDF at: {sumatra_path}")
                    logger.info(f"🖨️ Using SumatraPDF to print PDF to {printer_name}...")
                    cmd = [sumatra_path, "-print-to", printer_name, "-silent", pdf_path]
                    result = subprocess.run(cmd, capture_output=True)
                    if result.returncode == 0:
                        logger.info(f"✅ PDF printed successfully using SumatraPDF to {printer_name}")
                        return True
                    else:
                        logger.warning(f"⚠️ SumatraPDF failed: {result.stderr}")
                else:
                    logger.debug(f"   ❌ Not found")

            # Method 2: Try Windows ShellExecute
            logger.info("SumatraPDF not found, trying Windows ShellExecute...")
            try:
                import win32api
                win32api.ShellExecute(
                    0,
                    "print",
                    pdf_path,
                    f'/d:"{printer_name}"',
                    ".",
                    0
                )
                logger.info(f"✅ PDF sent to printer using ShellExecute: {printer_name}")
                import time
                time.sleep(1)
                return True
            except Exception as shell_error:
                logger.warning(f"⚠️ ShellExecute failed: {shell_error}")
                logger.info("🔄 Trying alternative method: Raw PDF printing...")

            # Method 3: Send raw PDF bytes to printer using win32print
            # This is more reliable when ShellExecute fails
            logger.info("📄 Using win32print to send raw PDF data...")

            # Read PDF file as binary
            with open(pdf_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # Open printer
            hprinter = win32print.OpenPrinter(printer_name)

            try:
                # Start a print job
                job_id = win32print.StartDocPrinter(hprinter, 1, (os.path.basename(pdf_path), None, "RAW"))
                logger.info(f"Started print job {job_id} on {printer_name}")

                # Start the first page
                win32print.StartPagePrinter(hprinter)

                # Send PDF data to printer
                win32print.WritePrinter(hprinter, pdf_data)
                logger.info(f"Sent {len(pdf_data)} bytes to printer")

                # End the page and document
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)

                logger.info(f"✅ PDF printed successfully using raw printer method")
                return True

            except Exception as raw_error:
                logger.error(f"❌ Raw printing also failed: {raw_error}")
                import traceback
                logger.error(traceback.format_exc())
                return False
            finally:
                win32print.ClosePrinter(hprinter)

        except Exception as e:
            logger.error(f"❌ Error printing PDF file: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def _print_html(self, hdc, data, page_width, page_height):
        """Print HTML content by converting to PDF first"""
        pdf_path = None
        try:
            html_content = data.get('html', data.get('content', ''))

            if not html_content:
                logger.warning("No HTML content provided")
                return

            # Convert HTML to PDF
            logger.info("Converting HTML to PDF...")
            pdf_path = self._convert_html_to_pdf(html_content)

            if not pdf_path or not os.path.exists(pdf_path):
                raise Exception("Failed to create PDF from HTML")

            # End the current document (we'll print the PDF separately)
            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()

            # Get printer name from data
            printer_name = data.get('printer_name', self.default_printer)

            # Print the PDF file
            logger.info(f"Printing PDF to {printer_name}...")
            self._print_pdf_file(pdf_path, printer_name)

            logger.info("HTML printed successfully via PDF conversion")

        except Exception as e:
            logger.error(f"Error printing HTML: {str(e)}")
            # Fallback: try to print as text
            logger.warning("Falling back to text-only printing")
            try:
                from bs4 import BeautifulSoup
                html_content = data.get('html', data.get('content', ''))
                soup = BeautifulSoup(html_content, 'html.parser')
                text = soup.get_text()

                normal_font = win32ui.CreateFont({
                    "name": "Courier New",
                    "height": 30,
                    "weight": 400,
                })
                hdc.SelectObject(normal_font)

                y_pos = 50
                for line in text.split('\n'):
                    if line.strip():
                        hdc.TextOut(50, y_pos, line.strip()[:80])
                        y_pos += 40
                        if y_pos > page_height - 100:
                            hdc.EndPage()
                            hdc.StartPage()
                            y_pos = 50
            except Exception as fallback_error:
                logger.error(f"Fallback printing also failed: {str(fallback_error)}")

        finally:
            # Clean up temporary PDF file
            if pdf_path and os.path.exists(pdf_path):
                try:
                    # Wait a bit for the print job to be spooled
                    import time
                    time.sleep(2)
                    os.remove(pdf_path)
                    logger.info(f"Cleaned up temporary PDF: {pdf_path}")
                except Exception as e:
                    logger.warning(f"Could not delete temporary PDF: {str(e)}")

    def add_to_queue(self, data, printer_name):
        """Add failed print job to queue"""
        queue_item = {
            'timestamp': datetime.now(),
            'data': data,
            'printer_name': printer_name,
            'status': 'pending'
        }
        self.print_queue.append(queue_item)
        logger.info(f"Added to queue: {printer_name} (Queue size: {len(self.print_queue)})")

    def get_queue(self):
        """Get current print queue including Windows spooler jobs"""
        combined_queue = list(self.print_queue)  # Start with our internal queue

        # Add jobs from Windows print spooler for all printers
        try:
            available_printers = self.get_available_printers()
            for printer_info in available_printers:
                printer_name = printer_info['name'] if isinstance(printer_info, dict) else printer_info
                try:
                    handle = win32print.OpenPrinter(printer_name)
                    jobs = win32print.EnumJobs(handle, 0, -1, 1)
                    win32print.ClosePrinter(handle)

                    for job in jobs:
                        # Add Windows spooler job to queue
                        queue_item = {
                            'timestamp': datetime.now(),
                            'data': {
                                'document_name': job.get('pDocument', 'Unknown'),
                                'type': 'text',
                                'content': f"Document from Windows Spooler\nJob ID: {job.get('JobId', 'N/A')}"
                            },
                            'printer_name': printer_name,
                            'status': 'spooler',
                            'job_id': job.get('JobId'),
                            'spooler_status': job.get('Status', 0),
                            'pages': job.get('TotalPages', 0),
                            'size': job.get('Size', 0)
                        }
                        combined_queue.append(queue_item)
                except Exception as e:
                    logger.debug(f"Could not get jobs for {printer_name}: {str(e)}")

        except Exception as e:
            logger.error(f"Error getting Windows spooler jobs: {str(e)}")

        return combined_queue

    def retry_queue_item(self, index):
        """Retry a specific queue item"""
        if 0 <= index < len(self.print_queue):
            item = self.print_queue[index]
            result = self.print_document(item['data'], item['printer_name'])
            if result:
                self.print_queue.pop(index)
                logger.info(f"Queue item {index} printed successfully")
                return True
            else:
                item['status'] = 'failed'
                logger.warning(f"Queue item {index} failed again")
                return False
        return False

    def clear_queue(self):
        """Clear the print queue"""
        count = len(self.print_queue)
        self.print_queue.clear()
        logger.info(f"Cleared {count} items from queue")
        return count

    def cancel_spooler_job(self, printer_name, job_id):
        """Cancel a job in Windows print spooler"""
        try:
            handle = win32print.OpenPrinter(printer_name)
            win32print.SetJob(handle, job_id, 0, None, win32print.JOB_CONTROL_DELETE)
            win32print.ClosePrinter(handle)
            logger.info(f"Cancelled spooler job {job_id} on {printer_name}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling spooler job: {str(e)}")
            return False

    def test_printer(self):
        """Test the printer with a simple message"""
        test_data = {
            'type': 'text',
            'document_name': 'Printer Test',
            'content': f'Printer Test\n\nDate: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\nPrinter is working correctly!'
        }
        return self.print_document(test_data)
