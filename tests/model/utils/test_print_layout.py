import pytest
from pytest_bdd import given, when, then, scenarios
from uidom.model import Button, Widget, Window
from uidom.model.utils.print import print_layout

scenarios("features/print_button_layout.feature")

@pytest.fixture
def widgets() -> list[Widget|Window]:
    return []

@given("a button with the following text")
def given_a_button_with_the_following_text(docstring: str, widgets: list[Widget|Window]) -> None:
    widgets.append(Button(text=docstring))

@when("the layout is printed", target_fixture="printed_layout")
def when_the_layout_is_printed(widgets: list[Widget|Window]) -> str:
    assert len(widgets) >= 1
    return print_layout(widgets[0])

@then("the following layout should be printed")
def then_the_following_layout_should_be_printed(docstring: str, printed_layout: str) -> None:
    assert docstring == printed_layout
