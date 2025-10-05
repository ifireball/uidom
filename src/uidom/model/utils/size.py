from functools import cache
from typing import Callable
from more_itertools import chunked
import cpmpy as cp
from cpmpy.expressions.variables import _IntVarImpl
from uidom.model import Widget, Window, Button
from uidom.model.layouts import GridLayout
from uidom.model.utils import Visitable


MAX_WIDGET_WIDTH = 80
MAX_WIDGET_HEIGHT = 40


class ModelSizer:
    """
    Calculate widget sizes.
    """
    def __init__(self, model: Widget|Window):
        self._model = model
        self._wv: Callable[[Visitable], _IntVarImpl] = cache(self._mk_width_var)
        self._hv: Callable[[Visitable], _IntVarImpl] = cache(self._mk_height_var)
        self._cp_model = cp.Model()
        self._cp_model_solved = False

    def width(self, model: Widget|Window) -> int:
        self._calculate_sizes()
        value = self._wv(model).value()
        if value is None:
            raise ValueError(f"Width not found for {model}")
        return value
    
    def height(self, model: Widget|Window) -> int:
        self._calculate_sizes()
        value = self._hv(model).value()
        if value is None:
            raise ValueError(f"Height not found for {model}")
        return value

    def _calculate_sizes(self) -> None:
        if self._cp_model_solved:
            return
        self._model.visit(self._get_widget_size_constraints)
        self._cp_model.minimize(self._wv(self._model) * self._hv(self._model))
        if self._cp_model.solve():
            self._cp_model_solved = True
            return
        raise ValueError(f"Failed to determine widget sizes for model, does it fit in ({MAX_WIDGET_WIDTH}x{MAX_WIDGET_HEIGHT})?")     

    def _get_widget_size_constraints(self, model: Visitable, *args: Visitable) -> Visitable:
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

                    self._cp_model += cp.AllEqual((self._wv(model) - 2) // columns, *(self._wv(arg) for arg in args))
                    self._cp_model += self._hv(model) == cp.sum(cp.max(self._hv(arg) for arg in chunk) for chunk in chunked(args, columns)) + 2 
            case _:
                raise NotImplementedError(f"Getting the size constraints of {model.__class__.__name__} is not implemented")
        return model

    @staticmethod
    def _mk_width_var(model: Visitable) -> _IntVarImpl:
        match model:
            case Button():
                var = cp.intvar(len(model.text) + 4, MAX_WIDGET_WIDTH)
            case Window():
                var = cp.intvar(len(model.title) + 6, MAX_WIDGET_WIDTH)
            case _:
                raise ValueError(f"Unknown model type: {model.__class__.__name__}")
        assert isinstance(var, _IntVarImpl)
        return var

    @staticmethod
    def _mk_height_var(model: Visitable) -> _IntVarImpl:
        match model:
            case Button():
                var = cp.intvar(3, MAX_WIDGET_HEIGHT)
            case Window():
                var = cp.intvar(3, MAX_WIDGET_HEIGHT)
            case _:
                raise ValueError(f"Unknown model type: {model.__class__.__name__}")
        assert isinstance(var, _IntVarImpl)
        return var
