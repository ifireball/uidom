from typing import Any
from uidom.model import Button, Window, Widget
from functools import singledispatchmethod
from uidom.model.utils.position import ModelPositioner
from uidom.model.utils.strcanvas import StrCanvas

def print_layout(model: Widget|Window) -> str:
    return LayoutPrinter(model).print()


_WINDOW_BORDER = b'#' * 8
_BUTTON_BORDER = rb'/-\|/-\|'


class LayoutPrinter:
    def __init__(self, model: Widget|Window):
        self._model = model
        self._positioner = ModelPositioner(model)
        self._canvas = StrCanvas(self._width(model), self._height(model))

    def print(self) -> str:
        self._model.visit(self._print_widget_layout)
        return str(self._canvas)

    @singledispatchmethod
    def _print_widget_layout(self, model: Widget|Window, *_: Any) -> None:
        raise NotImplementedError(f"Printing the layout of {model.__class__.__name__} is not implemented")

    @_print_widget_layout.register
    def _(self, model: Button, *_: Any) -> None:
        self._canvas.draw_border(self._left(model), self._top(model), self._width(model), self._height(model), border=_BUTTON_BORDER)
        self._canvas.draw_text(self._left(model) + 1, self._top(model) + 1, model.text.center(self._width(model) - 2, ' '))

    @_print_widget_layout.register
    def _(self, model: Window, *_: Any) -> None:
        model_width = self._width(model)
        self._canvas.draw_border(self._left(model), self._top(model), model_width, self._height(model), border=_WINDOW_BORDER)
        self._canvas.draw_text(self._left(model), self._top(model), f" {model.title} ".center(model_width, '#'))

    def _width(self, model: Widget|Window) -> int:
        return self._positioner.width(model)
    
    def _height(self, model: Widget|Window) -> int:
        return self._positioner.height(model)
    
    def _left(self, model: Widget|Window) -> int:
        return self._positioner.left(model)
    
    def _top(self, model: Widget|Window) -> int:
        return self._positioner.top(model)
