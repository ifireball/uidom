from .widget import Widget

class Button(Widget):
    """
    Represents a button on the screen.
    """
    def __init__(self, label: str):
        self.label = label
