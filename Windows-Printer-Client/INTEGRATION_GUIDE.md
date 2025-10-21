# Integration Guide: Backend-Socket ↔ Windows Printer Client

## Architecture Overview

```
Backend-Socket Server (Port 5001)
         ↓ WebSocket
Windows Printer Client
         ↓
Windows Printer (Thermal/Standard)
```

## Setup Steps

### 1. Configure Backend-Socket

The Backend-Socket server has been updated with a `print_response` handler in [app_socket.py:177-185](../Backend-Socket/app_socket.py#L177-L185).

### 2. Configure Windows Printer Client

Edit `.env` file:
```env
SOCKET_URL=http://localhost:5001
SESSION_ID=printer_client_session_001
USERNAME=printer_client
NIPT=your_company_nipt
```

### 3. Start Both Applications

**Terminal 1 - Backend-Socket:**
```bash
cd c:\Users\user\Desktop\ParidBackend\Backend-Socket
# Activate your venv and start the server
python app_socket.py
```

**Terminal 2 - Printer Client:**
```bash
cd c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client
venv\Scripts\activate
python printer_client.py
```

Or simply double-click `start_printer_client.bat`

## Triggering Prints from Your Backend

### Method 1: Direct Print Request

Add this to your Backend-Socket code wherever you need to print:

```python
from socketio_instance import socketio

# Simple text print
socketio.emit('print_request', {
    'data': {
        'type': 'text',
        'document_name': 'Order Confirmation',
        'content': 'Order #12345\nCustomer: John Doe\nTotal: $50.00'
    }
}, broadcast=True)
```

### Method 2: POS Receipt Print

```python
from socketio_instance import socketio

# Trigger when POS transaction completes
socketio.emit('print_request', {
    'data': {
        'type': 'receipt',
        'receipt_data': {
            'date': '2025-01-15',
            'receipt_number': 'RCP-001',
            'customer_name': 'John Doe',
            'items': [
                {'name': 'Coffee', 'quantity': 2, 'price': 3.50},
                {'name': 'Sandwich', 'quantity': 1, 'price': 5.99}
            ],
            'total': 12.99,
            'footer': 'Thank you!'
        }
    }
}, broadcast=True)
```

### Method 3: Reservation Confirmation

```python
from socketio_instance import socketio

# Trigger when reservation is created
socketio.emit('print_request', {
    'data': {
        'type': 'reservation',
        'reservation_data': {
            'confirmation_number': 'RES-12345',
            'customer_name': 'Jane Smith',
            'date': '2025-01-20',
            'time': '19:00',
            'party_size': '4',
            'table_number': '12',
            'phone': '+1234567890'
        }
    }
}, broadcast=True)
```

## Integration Examples

### Example 1: Print on POS Completion

In your POS controller (`controllers/_pos.py`):

```python
from socketio_instance import socketio

def complete_pos_transaction(pos_data):
    # Your existing POS logic
    # ...

    # Trigger print
    socketio.emit('print_request', {
        'data': {
            'type': 'receipt',
            'receipt_data': pos_data
        }
    }, broadcast=True)

    return {"status": "success"}
```

### Example 2: Print on Reservation Creation

In your reservation controller (`controllers/_reservation.py`):

```python
from socketio_instance import socketio

def create_reservation(reservation_data):
    # Your existing reservation logic
    # Save to database, etc.

    # Trigger print
    if reservation_data.get('print_confirmation'):
        socketio.emit('print_request', {
            'data': {
                'type': 'reservation',
                'reservation_data': reservation_data
            }
        }, broadcast=True)

    return {"status": "success"}
```

### Example 3: Using the Example Script

See [example_print_trigger.py](../Backend-Socket/example_print_trigger.py) for ready-to-use functions:

```python
from example_print_trigger import send_receipt_print, send_reservation_print

# In your code
if payment_successful:
    send_receipt_print()
```

## WebSocket Events

### Events Sent by Backend-Socket

| Event | Description | Data Format |
|-------|-------------|-------------|
| `print_request` | Request to print a document | `{data: {type, document_name, content/receipt_data/reservation_data}}` |
| `pos` | POS update (can include print flag) | `{nipt, pos_data: {print_required, ...}}` |
| `reservation` | Reservation update (can include print flag) | `{nipt, reservation_data: {print_required, ...}}` |

### Events Received by Backend-Socket

| Event | Description | Data Format |
|-------|-------------|-------------|
| `print_response` | Acknowledgment of print job | `{status, message, timestamp, printer}` |

## Testing the Integration

### 1. Start Both Applications

Make sure both Backend-Socket and Windows Printer Client are running.

### 2. Test with Python Console

Open a Python console in Backend-Socket directory:

```python
python
>>> from app_socket import socketio
>>> socketio.emit('print_request', {
...     'data': {
...         'type': 'text',
...         'content': 'Integration Test Success!'
...     }
... }, broadcast=True)
```

### 3. Check Logs

**Backend-Socket logs:** Should show print_response received
**Printer Client logs:** Check `printer_client.log`
**Printer:** Should have printed the test

## Troubleshooting

### Printer Client Not Connecting

1. Check Backend-Socket is running: `http://localhost:5001`
2. Verify `.env` configuration in Printer Client
3. Check session_id, username, nipt match expected values
4. Review Backend-Socket logs for connection attempts

### Print Not Triggering

1. Check Printer Client logs: `type printer_client.log`
2. Verify event name is exactly `print_request`
3. Ensure `broadcast=True` is set in emit
4. Check printer is turned on and has paper

### Print Format Issues

1. For thermal printers, content may need formatting adjustment
2. Modify `printer_handler.py` print methods as needed
3. Test with simple text first, then complex receipts

## Advanced Configuration

### Multiple Printers

To route prints to different printers:

```python
# In Backend-Socket
socketio.emit('print_request', {
    'data': {...},
    'printer_name': 'Specific Printer Name'  # Optional
}, broadcast=True)
```

### Auto-start on Windows Boot

See [README.md](README.md#auto-start-on-windows-startup-optional) for Task Scheduler setup.

### Custom Print Formats

Edit `printer_handler.py` methods:
- `_print_text()` - Simple text
- `_print_receipt()` - Receipt format
- `_print_reservation()` - Reservation format

## Production Deployment

1. **Run as Windows Service:**
   - Install NSSM (Non-Sucking Service Manager)
   - Create service pointing to `venv\Scripts\python.exe printer_client.py`

2. **Monitoring:**
   - Set up log rotation for `printer_client.log`
   - Monitor for reconnection attempts
   - Alert on persistent failures

3. **Security:**
   - Use environment-specific NIPT values
   - Secure WebSocket connection with SSL in production
   - Restrict network access to Backend-Socket server

## Support

For issues or questions:
1. Check logs in both applications
2. Review this integration guide
3. Test printer connectivity with `python printer_test.py`
4. Contact development team
