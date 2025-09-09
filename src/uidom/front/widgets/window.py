from psygnal import Signal

class Window:
    """
    Represents a window on the screen.
    """
    closed = Signal()
    
    def __init__(self, title: str):
        self.title = title

    def close(self) -> None:
        self.closed.emit()
