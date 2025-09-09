import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import time
from gi.repository import GLib

def test_window_display(window):
    """Test if the window is actually being displayed"""
    print(f"Window title: '{window.get_title()}'")
    print(f"Window visible: {window.get_visible()}")
    print(f"Window mapped: {window.get_mapped()}")
    print(f"Window realized: {window.get_realized()}")
    
    # Get window geometry
    allocation = window.get_allocation()
    print(f"Window size: {allocation.width}x{allocation.height}")
    
    # Check if window is on screen
    display = window.get_display()
    if display:
        print(f"Window on display: {display is not None}")
    
    is_active = window.is_active() if hasattr(window, "is_active") else "N/A"
    print(f"Window is active: {is_active}")
    
    return window.get_visible() and window.get_mapped()

def main():
    # Create a window
    window = Gtk.Window()
    window.set_title("Minimal GTK Window")
    # window.set_default_size(400, 300)
    # window.set_position(Gtk.WindowPosition.CENTER)
    
    # Connect the destroy event (optional for this minimal example)
    # window.connect("destroy", lambda w: None)
    
    # Show the window
    window.present()
    print("Window created and shown...")
    
    # Process events multiple times to ensure window is displayed
    for i in range(2):  # Give GTK several chances to display the window
        # In Gtk 4, events_pending() and main_iteration() are removed.
        # Instead, you can use GLib's main context iteration.
        while GLib.MainContext.default().iteration(False):
            pass
        time.sleep(0.01)  # Small delay to allow rendering
    
    print("Window should be visible now!")
    
    # Test if window is actually displayed
    is_displayed = test_window_display(window)
    print(f"Window display test result: {'PASS' if is_displayed else 'FAIL'}")
    
    print("Press enter to exit...")
    input()
        
    # Clean up and exit
    # window.destroy()
    print("Exiting...")

if __name__ == "__main__":
    main()
