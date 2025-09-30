from math import ceil, floor
from uidom.model import Button, Window
from uidom.model.utils.visit import Visitable
from functools import singledispatch

def print_layout(model: Visitable) -> str:
    return model.visit(print_widget_layout)

@singledispatch
def print_widget_layout(model: Visitable, *args: str) -> str:
    raise NotImplementedError(f"Printing the layout of {model.__class__.__name__} is not implemented")

@print_widget_layout.register
def _(model: Button, *args: str) -> str:
    border_length = len(model.text) + 2
    return "\n".join((
        f"/{'-' * border_length}\\",
        f"| {model.text} |",
        f"\\{'-' * border_length}/"
    ))

@print_widget_layout.register
def _(model: Window, *args: str) -> str:
    content = args[0]
    content_width = max(len(line) for line in content.splitlines())
    return "\n".join((
        f"{'#' * ceil((content_width - len(model.title)) / 2)} {model.title} {'#' * floor((content_width - len(model.title)) / 2)}",
        *(f"#{line}#" for line in content.splitlines()),
        f"{'#' * (content_width + 2)}"
    ))
