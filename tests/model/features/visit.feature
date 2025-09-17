Feature: Visit
    The UI DOM structure implements the Visitor pattern.

    Scenario: Visit the UI DOM structure
        Given a UI DOM structure
        And a visitor function
        When the structure is visited with the visitor function
        Then each element should be visited in DFS order
