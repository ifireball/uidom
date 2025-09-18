from pytest_bdd import given, when, then, scenarios
from uidom.model import Button
from uidom.model.utils.print import print_layout

scenarios("features/print_button_layout.feature")

@given("a button with the following text", target_fixture="button")
def given_a_button_with_the_following_text(docstring: str) -> Button:
    return Button(text=docstring)

@when("the layout is printed", target_fixture="printed_layout")
def when_the_layout_is_printed(button: Button) -> str:
    return print_layout(button)

@then("the following layout should be printed")
def then_the_following_layout_should_be_printed(docstring: str, printed_layout: str) -> None:
    assert docstring == printed_layout
