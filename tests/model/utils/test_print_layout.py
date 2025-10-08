import pytest
from pytest_bdd import given, when, then, scenarios
from uidom.model import Button, Widget, Window
from uidom.model.style import Style
from uidom.model.layouts import GridLayout
from uidom.model.positions import GridPosition
from uidom.model.utils.print import print_layout
from typing import Callable

scenarios(
    "features/print_button_layout.feature",
    "features/print_window_layout.feature"
)

@pytest.fixture
def widgets() -> list[Widget|Window]:
    return []

@given("a button with the following text")
def given_a_button_with_the_following_text(docstring: str, widgets: list[Widget|Window]) -> None:
    widgets.append(Button(text=docstring))

@given("a button")
@given("another button")
def given_a_button(widgets: list[Widget|Window], enumerated_title: Callable[[str], str]) -> None:
    widgets.append(Button(text=enumerated_title("Button")))

@given("another button with horizontal span of 2")
def given_another_button_with_horizontal_span_of_2(widgets: list[Widget|Window], enumerated_title: Callable[[str], str]) -> None:
    widgets.append(Button(text=enumerated_title("Button"), style=Style(position=GridPosition(horizontal_span=2))))

@given("it is embedded in a window with a grid layout")
def given_it_is_embedded_in_a_window(widgets: list[Widget|Window], enumerated_title: Callable[[str], str]) -> None:
    window_widgets = tuple(w for w in widgets if isinstance(w, Widget))
    widgets.clear()
    widgets.append(Window(title=enumerated_title("Window"), widgets=window_widgets, style=Style(layout=GridLayout())))

@given("it is embedded in a window with the following title")
def given_it_is_embedded_in_a_window_with_the_following_title(docstring: str, widgets: list[Widget|Window]) -> None:
    window_widgets = tuple(w for w in widgets if isinstance(w, Widget))
    widgets.clear()
    widgets.append(Window(title=docstring, widgets=window_widgets))

@when("the layout is printed", target_fixture="printed_layout")
def when_the_layout_is_printed(widgets: list[Widget|Window]) -> str:
    assert len(widgets) >= 1
    return print_layout(widgets[0])

@then("the following layout should be printed")
def then_the_following_layout_should_be_printed(docstring: str, printed_layout: str) -> None:
    assert printed_layout == docstring
