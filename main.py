import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import time

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
    screen = window.get_screen()
    if screen:
        print(f"Window on screen: {screen.get_display() is not None}")
    
    # Test window state
    state = window.get_state()
    print(f"Window state: {state}")
    
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
    window.show_all()
    print("Window created and shown...")
    
    # Process events multiple times to ensure window is displayed
    for i in range(2):  # Give GTK several chances to display the window
        while Gtk.events_pending():
            Gtk.main_iteration()
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
