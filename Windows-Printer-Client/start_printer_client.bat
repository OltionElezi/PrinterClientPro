@echo off
echo Starting Windows Printer Client...
cd /d "c:\Users\user\Desktop\ParidBackend\Windows-Printer-Client"
call venv\Scripts\activate
python printer_client.py
pause
