# Print Client Pro - Smart Startup Behavior

## Overview

Print Client Pro now features intelligent startup behavior that keeps the app running in the background without showing the window unnecessarily.

## Smart Startup Features

### 1. Auto-Connect on Window Open
- **Every time the window opens**, the app automatically attempts to connect to the server
- No need to manually click the "Connect" button
- Happens 500ms after window opens for smooth UI experience

### 2. Smart Startup Behavior (Auto-Hide)
When the app starts with Windows:
- Window opens and immediately tries to connect
- After **10 seconds**:
  - ✅ **If connected successfully**: Window automatically hides to system tray
  - ❌ **If connection failed**: Window stays visible so user can see the problem

### 3. Manual Window Opening
When you click the tray icon to open the window:
- Window shows immediately
- If disconnected, automatically tries to reconnect
- Window stays visible (doesn't auto-hide)
- You can manually close it when done

## Behavior Scenarios

### Scenario 1: PC Startup - Connection Succeeds
```
1. Windows boots
2. PrintClientPro starts automatically
3. Window appears briefly
4. App connects to server (within 10 seconds)
5. Window automatically hides to tray
6. App continues running in background
```
**User sees**: Brief window flash, then just tray icon

### Scenario 2: PC Startup - Connection Fails
```
1. Windows boots
2. PrintClientPro starts automatically
3. Window appears
4. App tries to connect to server
5. Connection fails
6. After 10 seconds, window STAYS VISIBLE
7. User can see error and fix configuration
```
**User sees**: Window with connection error, can troubleshoot

### Scenario 3: User Opens Window Manually
```
1. User clicks tray icon
2. Window opens
3. If disconnected, auto-reconnects
4. Window stays visible
5. User can monitor, configure, etc.
6. User closes window manually
```
**User sees**: Normal window behavior, auto-reconnect on open

### Scenario 4: User Reopens After Hiding
```
1. User clicks tray icon (after window was hidden)
2. Window appears
3. If connection was lost, automatically tries to reconnect
4. Window stays visible until user closes it
```
**User sees**: Window with auto-reconnect attempt

## Auto-Reconnect Behavior

### When Auto-Reconnect Triggers:
1. **Window opens and not connected**: Tries to connect
2. **Window already open**: No auto-reconnect (user can use Connect button)
3. **First startup**: Auto-connects and auto-hides if successful

### Reconnection Timing:
- Waits 500ms after window opens before attempting connection
- Allows UI to fully initialize
- Smooth user experience

## User Experience

### Normal Daily Use:
1. PC boots → App starts → Auto-hides (if connected) → Runs in tray
2. Print jobs process automatically in background
3. User never needs to interact with the app
4. Tray icon shows app is running

### Troubleshooting:
1. PC boots → App starts → Connection fails → Window stays visible
2. User sees error message
3. Can fix configuration or check server
4. Click Connect to retry
5. Close window when fixed

### Manual Monitoring:
1. User wants to check status
2. Clicks tray icon → Window opens
3. Can view logs, queue, printers
4. If was disconnected, auto-reconnects
5. User closes window when done

## Configuration

No configuration needed! The smart behavior is automatic.

### Customization (Advanced):
If you want to change the 10-second timeout, edit `printer_client_tray.py`:

```python
# Change this line (currently 10000ms = 10 seconds):
self.gui_window.after(10000, self.check_connection_and_hide)

# Example: 5 seconds
self.gui_window.after(5000, self.check_connection_and_hide)

# Example: 15 seconds
self.gui_window.after(15000, self.check_connection_and_hide)
```

## Technical Details

### Implementation:
1. **`is_startup` flag**: Tracks if this is the initial app startup
2. **`auto_hide_on_connect` parameter**: Passed to `show_gui()` on startup
3. **`check_connection_and_hide()` method**: Called after 10 seconds
   - Checks if connected
   - Checks if still in startup mode
   - Hides window if both are true
4. **Auto-connect**: Triggered on any window open via `after(500, connect_to_server)`

### Code Flow:
```python
# On startup:
run() → show_gui(auto_hide_on_connect=True) →
  after(500, connect_to_server) →  # Try to connect
  after(10000, check_connection_and_hide) →  # Check after 10s
  if connected: hide_gui()

# On manual open:
show_gui() (no auto_hide_on_connect) →
  after(500, connect_to_server) →  # Try to connect
  window stays visible

# On reopen existing window:
deiconify() →
  if not connected: after(500, connect_to_server) →
  window stays visible
```

## Benefits

### For End Users:
- ✅ **Less intrusive**: App doesn't clutter screen on startup
- ✅ **Auto-healing**: Reconnects automatically when window opens
- ✅ **Visual feedback**: Window stays visible if there's a problem
- ✅ **Convenient**: No manual connecting needed

### For IT Support:
- ✅ **Self-diagnosing**: Problems are visible (window stays open)
- ✅ **Less support calls**: Users don't need to manually connect
- ✅ **Better UX**: Professional auto-hide behavior
- ✅ **Reliable**: Always tries to connect on window open

## Testing

### Test Auto-Hide on Startup:
1. Ensure server is running and accessible
2. Restart your PC
3. App should start, connect, and hide automatically
4. Check tray - app should be running there

### Test Manual Open:
1. Click tray icon
2. Window should open
3. If disconnected, should auto-connect
4. Window stays visible
5. Close manually

### Test Connection Failure:
1. Stop your server (or disconnect network)
2. Restart PC
3. App should start and try to connect
4. After 10 seconds, window should STAY VISIBLE
5. Error should be visible in console log

## Summary

PrintClientPro now provides a seamless background experience:

- **Silent success**: Connects and hides automatically on startup
- **Visible failures**: Shows window when something needs attention
- **Auto-reconnect**: Always tries to connect when window opens
- **User control**: Manual window opening works as expected

This creates a professional, low-maintenance experience for end users while ensuring problems are visible when they occur.
