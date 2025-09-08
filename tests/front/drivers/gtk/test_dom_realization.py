from pytest_bdd import given, when, then, scenario
from uidom.front import Application, Window

@scenario("features/dom_realization.feature", "Realize a Window")
def test_realize_a_window():
    pass

@given("a UI DOM structure with a Window")
def given_a_ui_dom_structure_with_a_window(dom_application: Application):
    dom_application.windows.append(Window())

@when("the structure is realized")
def when_the_structure_is_realized():
    pass

@then("the Window should be visible on screen")
def then_the_window_should_be_visible_on_screen():
    pass

