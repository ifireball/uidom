from textwrap import dedent
from uidom.model.widgets import Button
from uidom.model.utils.visit import Visitable

def print_layout(model: Visitable) -> str:
    return model.visit(print_widget_layout)

def print_widget_layout(model: Visitable, *args: str) -> str:
    if isinstance(model, Button):
        border_length = len(model.text) + 2
        return "\n".join((
            f"/{'-' * border_length}\\",
            f"| {model.text} |",
            f"\\{'-' * border_length}/"
        ))
    return ""

