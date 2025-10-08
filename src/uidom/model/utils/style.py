from typing import Any, Collection
from dataclasses import dataclass
from uidom.model.widgets import Widget
from uidom.model.positions import GridPosition
from uidom.model.layouts import GridLayout
from uidom.model.style import Styleable


def colspan(widget: Any) -> int:
    """
    Return the horizontal span of a widget within a grid layout.

    >>> from uidom.model import Button
    >>> from uidom.model.style import Style
    >>> from uidom.model.positions import GridPosition
    >>> colspan(Button(style=Style(position=GridPosition(horizontal_span=2))))
    2

    >>> colspan(Button())
    1

    We use very lax typing here to make this helper useful in various places.

    >>> colspan(object())
    1
    """
    match widget:
        case Styleable():
            match widget.style.position:
                case GridPosition(horizontal_span=span):
                    return span
    return 1


@dataclass(frozen=True)
class SpanPlaceholder:
    widget: Widget


class ColSpanPlaceholder(SpanPlaceholder):
    pass


def layout_grid(widgets: Collection[Widget], layout: GridLayout) -> list[list[Widget|SpanPlaceholder]]:
    """
    Break down a grid layout into a matrix indicating for each cell what widget
    should be placed there, or wither a widget is spanning into it.

    >>> from uidom.model.widgets import Button
    >>> from uidom.model.layouts import GridLayout
    >>> from uidom.model.style import Style
    >>> from uidom.model.positions import GridPosition

    >>> b1, b2, b3 = Button(text="b1"), Button(text="b2"), Button(text="b3")
    >>> hsb1 = Button(style=Style(position=GridPosition(horizontal_span=2)), text="hsb1")

    >>> layout_grid([b1, b2, b3], GridLayout(size=2)) == [[b1, b2], [b3]]
    True
    >>> layout_grid([b1, b2, hsb1], GridLayout(size=2)) == [[b1, b2], [hsb1, ColSpanPlaceholder(widget=hsb1)]]
    True
    >>> layout_grid([hsb1, b1, b2], GridLayout(size=2)) == [[hsb1, ColSpanPlaceholder(widget=hsb1)], [b1, b2]]
    True
    >>> layout_grid([b1, hsb1, b2], GridLayout(size=3)) == [[b1, hsb1, ColSpanPlaceholder(widget=hsb1)], [b2]]
    True
    >>> layout_grid([b1, hsb1, b2], GridLayout(size=2))
    Traceback (most recent call last):
    ...
    ValueError: Widgets to not fit in grid layout: 3 > 2
    """
    rows = []
    columns = []
    for widget in widgets:
        columns.append(widget)
        columns.extend(ColSpanPlaceholder(widget) for _ in range(1, colspan(widget)))
        if len(columns) == layout.size:
            rows.append(columns)
            columns = []
        elif len(columns) > layout.size:
            raise ValueError(f"Widgets to not fit in grid layout: {len(columns)} > {layout.size}")
    if columns:
        rows.append(columns)
    return rows
