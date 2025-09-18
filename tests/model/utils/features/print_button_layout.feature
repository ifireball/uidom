Feature: Print Button Layout
    Print the layout of a button.

    Scenario: Print the layout of a simple button
        Given a button with the following text
            """
            Button 1
            """
        When the layout is printed
        Then the following layout should be printed
            """
            /----------\
            | Button 1 |
            \----------/
            """
