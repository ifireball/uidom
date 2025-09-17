from pytest_bdd import given, when, then, scenario
from uidom.model import Application, Window, Button, StringDisplay
from uidom.model.utils import Visitor
from unittest.mock import MagicMock, call

# Note: Can't use scenarios() here because `call` messes up its scenario detection logic

@scenario("features/visit.feature", "Visit the UI DOM structure")
def test_visit():
    pass


@given("a UI DOM structure", target_fixture="dom_application")
def given_a_ui_dom_structure() -> Application:
    return Application(windows=frozenset([
        Window(widgets=(
            Button(text="Button 1"), 
            Button(text="Button 2"), 
            StringDisplay(text="String Display")
        ))
    ]))

@given("a visitor function", target_fixture="visitor")
def given_a_visitor_function() -> Visitor:
    visitor = MagicMock(spec=Visitor)
    # Note: We need to subtract 1 because the side effect is called after the mock call is counted
    visitor.side_effect = lambda *args, **kwargs: visitor.call_count - 1
    return visitor

@when("the structure is visited with the visitor function")
def when_the_structure_is_visited_with_the_visitor_function(dom_application: Application, visitor: Visitor) -> None:
    dom_application.visit(visitor)

@then("each element should be visited in DFS order")
def then_each_element_should_be_visited_in_DFS_order(dom_application: Application, visitor: MagicMock) -> None:
    dom_window = next(iter(dom_application.windows))
    assert visitor.call_args_list == [
        call(Button(text="Button 1")),
        call(Button(text="Button 2")), 
        call(StringDisplay(text="String Display")),
        call(dom_window, 0, 1, 2),
        call(dom_application, 3)
    ]
