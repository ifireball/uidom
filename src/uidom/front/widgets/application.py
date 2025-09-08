from .window import Window

class Application:
    """
    A top-level application container.
    """
    def __init__(self, windows: list[Window] = []):
        self.windows: list[Window] = windows
