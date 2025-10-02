from math import ceil, floor
from uidom.model import Button, Window, Widget
from uidom.model.utils.objrefkey import objRefKeySet, ObjRefKeyMaker, ObjRefKey
from functools import singledispatchmethod
from constraint import AllEqualConstraint, Problem, MinConflictsSolver
from uidom.model.utils.center import center

def print_layout(model: Widget|Window) -> str:
    return LayoutPrinter(model).print()

_MAX_WIDGET_WIDTH = 80
_MAX_WIDGET_HEIGHT = 40

class LayoutPrinter:
    def __init__(self, model: Widget|Window):
        self._model = model
        self._wk: ObjRefKeyMaker[Widget|Window] = objRefKeySet()
        self._hk: ObjRefKeyMaker[Widget|Window] = objRefKeySet()
        self._sizeProblem = Problem()
        self._modelSizes: dict[ObjRefKey[Widget|Window], int] = {}

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
        self._calculate_sizes()
        return self._modelSizes[self._wk(model)]
    
    def _height(self, model: Widget|Window) -> int:
        self._calculate_sizes()
        return self._modelSizes[self._hk(model)]

    def _calculate_sizes(self) -> None:
        if self._modelSizes:
            return
        self._model.visit(self._get_widget_size_constraints)
        solution = self._sizeProblem.getSolution()
        #solutions = self._sizeProblem.getSolutionIter()
        #solution = min(solutions, key=lambda sol: sol[self._wk(self._model)])
        if not solution:
            raise RuntimeError("No solution found for the widget size problem")
        self._modelSizes.update((k, v) for (k, v) in solution.items())

    @singledispatchmethod
    def _get_widget_size_constraints(self, model: Widget|Window, *args: Widget|Window) -> Widget|Window:
        raise NotImplementedError(f"Getting the size constraints of {model.__class__.__name__} is not implemented")

    @_get_widget_size_constraints.register
    def _(self, model: Button, *args: Widget|Window) -> Widget|Window:
        # Note: it seems python-constrain checks the domains in reverse order,
        # so in order to make the first solution found to contain the smallest
        # width and height, we need to add the smallest values last
        self._sizeProblem.addVariable(self._wk(model), range(_MAX_WIDGET_WIDTH, len(model.text) + 4 - 1, -1))
        self._sizeProblem.addVariable(self._hk(model), range(_MAX_WIDGET_HEIGHT, 2, -1))
        return model

    @_get_widget_size_constraints.register
    def _(self, model: Window, *args: Widget|Window) -> Widget|Window:
        self._sizeProblem.addVariable(self._wk(model), range(_MAX_WIDGET_WIDTH, len(model.title) + 6 - 1, -1))
        self._sizeProblem.addVariable(self._hk(model), range(_MAX_WIDGET_HEIGHT, 2, -1))
        if args:
            self._sizeProblem.addConstraint(AllEqualConstraint(), [self._wk(arg) for arg in args])
            self._sizeProblem.addConstraint(lambda win_w, widg_w: win_w == widg_w + 2, [self._wk(model), self._wk(args[0])])
            self._sizeProblem.addConstraint(lambda win_h, *widg_h: win_h == sum(widg_h) + 2, [self._hk(model), *(self._hk(w) for w in args)])
        return model
