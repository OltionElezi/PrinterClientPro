"""
Windows Printer Client - System Tray Application
Runs in background with system tray icon
"""
import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os
import time

# Import the main GUI
from printer_client_gui import PrinterClientGUI
import tkinter as tk

class PrinterClientTray:
    def __init__(self):
        self.gui_window = None
        self.gui_visible = False
        self.app = None
        self.is_startup = True  # Track if this is app startup

        # Create tray icon
        self.icon = self.create_icon()

        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem('Print Client Pro', self.show_gui, default=True),
            pystray.MenuItem('Show Window', self.show_gui),
            pystray.MenuItem('Hide Window', self.hide_gui),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', self.quit_app)
        )

        # Create system tray
        self.tray = pystray.Icon(
            "PrintClientPro",
            self.icon,
            "Print Client Pro",
            menu
        )

    def create_icon(self):
        """Create a printer icon for system tray"""
        # Create an image with a printer icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (15, 23, 42))  # Dark background
        dc = ImageDraw.Draw(image)

        # Draw printer icon (simplified)
        # Top part
        dc.rectangle([20, 15, 44, 25], fill=(99, 102, 241))  # Indigo
        # Middle part (main body)
        dc.rectangle([15, 25, 49, 45], fill=(241, 245, 249))  # Light
        # Paper slot
        dc.rectangle([22, 30, 42, 40], fill=(15, 23, 42))
        # Bottom part
        dc.rectangle([20, 45, 44, 50], fill=(16, 185, 129))  # Green

        return image

    def show_gui(self, icon=None, item=None):
        """Show the GUI window"""
        if not self.gui_window or not self.gui_window.winfo_exists():
            # Create new window
            self.gui_window = tk.Tk()
            self.app = PrinterClientGUI(self.gui_window)

            # Override close button to hide instead of quit
            self.gui_window.protocol("WM_DELETE_WINDOW", self.hide_gui)

            # Auto-connect when window opens
            if not self.app.connected:
                self.gui_window.after(500, self.app.connect_to_server)

            # If this is startup, check if we should auto-hide
            if self.is_startup:
                self.gui_window.after(10000, self.check_connection_and_hide)

            self.gui_visible = True
            self.gui_window.mainloop()
        else:
            # Show existing window
            self.gui_window.deiconify()
            self.gui_window.lift()
            self.gui_window.focus_force()
            self.gui_visible = True

            # Auto-reconnect if disconnected when reopening window
            if not self.app.connected:
                self.gui_window.after(500, self.app.connect_to_server)

    def check_connection_and_hide(self):
        """Check if connected after 10 seconds, hide window if connected"""
        if self.app and self.app.connected and self.is_startup:
            # Connected successfully, hide the window
            self.hide_gui()
        # If not connected, window stays visible
        self.is_startup = False  # No longer startup after first check

    def hide_gui(self, icon=None, item=None):
        """Hide the GUI window"""
        if self.gui_window and self.gui_window.winfo_exists():
            self.gui_window.withdraw()
            self.gui_visible = False

    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        # Disconnect from server if connected
        if self.gui_window and hasattr(self, 'app'):
            try:
                if self.app.connected:
                    self.app.sio.disconnect()
            except:
                pass

        # Stop tray icon
        self.tray.stop()

        # Destroy GUI window
        if self.gui_window and self.gui_window.winfo_exists():
            self.gui_window.quit()
            self.gui_window.destroy()

        sys.exit(0)

    def run(self):
        """Run the system tray application"""
        # Start GUI in background thread with smart startup behavior
        gui_thread = threading.Thread(target=self.show_gui, daemon=True)
        gui_thread.start()

        # Run tray icon (blocking)
        self.tray.run()

if __name__ == "__main__":
    app = PrinterClientTray()
    app.run()
