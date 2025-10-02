from math import ceil, floor
from uidom.model import Button, Window, Widget
from functools import singledispatchmethod
from uidom.model.utils.center import center
from uidom.model.utils.size import ModelSizer

def print_layout(model: Widget|Window) -> str:
    return LayoutPrinter(model).print()

_MAX_WIDGET_WIDTH = 80
_MAX_WIDGET_HEIGHT = 40

class LayoutPrinter:
    def __init__(self, model: Widget|Window):
        self._model = model
        self._sizer = ModelSizer(model)

    def print(self) -> str:
        return self._model.visit(self._print_widget_layout)

    @singledispatchmethod
    def _print_widget_layout(self, model: Widget|Window, *args: str) -> str:
        raise NotImplementedError(f"Printing the layout of {model.__class__.__name__} is not implemented")

    @_print_widget_layout.register
    def _(self, model: Button, *args: str) -> str:
        border_length = self._width(model) - 2
        return "\n".join((
            f"/{'-' * border_length}\\",
            f"|{center(model.text, border_length)}|",
            f"\\{'-' * border_length}/"
        ))

    @_print_widget_layout.register
    def _(self, model: Window, *args: str) -> str:
        model_width = self._width(model)
        return "\n".join((
            center(f" {model.title} ", model_width, '#'),
            *(f"#{line}#" for arg in args for line in arg.splitlines()),
            f"{'#' * (model_width)}"
        ))

    def _width(self, model: Widget|Window) -> int:
        return self._sizer.width(model)
    
    def _height(self, model: Widget|Window) -> int:
        return self._sizer.height(model)
