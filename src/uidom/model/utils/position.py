from functools import cache
from typing import Callable
import cpmpy as cp
from cpmpy.expressions.variables import _IntVarImpl
from uidom.model import Widget, Window, Button
from .size import MAX_WIDGET_WIDTH, MAX_WIDGET_HEIGHT, ModelSizer
from .visit import Visitable
from more_itertools import chunked
from uidom.model.layouts import GridLayout
from uidom.model.utils.style import colspan

class ModelPositioner:
    def __init__(self, model: Widget|Window):
        self._model = model
        self._sizer = ModelSizer(model)
        self._lv: Callable[[Visitable], _IntVarImpl] = cache(self._mk_left_var)
        self._tv: Callable[[Visitable], _IntVarImpl] = cache(self._mk_top_var)
        self._cp_model = cp.Model()
        self._cp_model_solved = False

    def width(self, model: Widget|Window) -> int:
        return self._sizer.width(model)
    
    def height(self, model: Widget|Window) -> int:
        return self._sizer.height(model)

    def left(self, model: Widget|Window) -> int:
        self._calculate_positions()
        value = self._lv(model).value()
        if value is None:
            raise ValueError(f"Left not found for {model}")
        return value
    
    def top(self, model: Widget|Window) -> int:
        self._calculate_positions()
        value = self._tv(model).value()
        if value is None:
            raise ValueError(f"Top not found for {model}")
        return value
    
    def _calculate_positions(self) -> None:
        if self._cp_model_solved:
            return
        self._model.visit(self._get_widget_position_constraints)
        self._cp_model += self._lv(self._model) == 0
        self._cp_model += self._tv(self._model) == 0
        if self._cp_model.solve():
            self._cp_model_solved = True
            return
        raise ValueError(f"Failed to determine widget positions for model, does it fit in ({MAX_WIDGET_WIDTH}x{MAX_WIDGET_HEIGHT})?")
    
    def _get_widget_position_constraints(self, model: Visitable, *args: Visitable) -> Visitable:
        match model:
            case Button():
                pass
            case Window():
                if args:
                    match model.style.layout:
                        case GridLayout(size=size):
                            columns = size
                        case _:
                            columns = 1
                        
                    top = 1
                    left = 1
                    column = 0
                    for widget in args:
                        assert isinstance(widget, Widget)
                        self._cp_model += self._lv(widget) == left
                        self._cp_model += self._tv(widget) == top
                        left += self.width(widget)
                        column += colspan(widget)
                        if column == columns:
                            column = 0
                            top += self.height(widget)
                            left = 1
            case _:
                raise NotImplementedError(f"Getting the position constraints of {model.__class__.__name__} is not implemented")
        return model

    def _mk_left_var(self, model: Widget|Window) -> _IntVarImpl:
        var = cp.intvar(0, MAX_WIDGET_WIDTH - self.width(model))
        assert isinstance(var, _IntVarImpl)
        return var
    
    def _mk_top_var(self, model: Widget|Window) -> _IntVarImpl:
        var = cp.intvar(0, MAX_WIDGET_HEIGHT - self.height(model))
        assert isinstance(var, _IntVarImpl)
        return var
