from .widget import Widget

class StringDisplay(Widget):
    """
    Represents a string display on the screen.
    Typically implemented wit a label or a disabled input field.
    """
    def __init__(self, text: str):
        self.text = text
