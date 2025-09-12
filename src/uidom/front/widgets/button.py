from .widget import Widget

class Button(Widget):
    """
    Represents a button on the screen.
    """
    def __init__(self, text: str):
        self.text = text
