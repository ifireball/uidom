Feature: UI Layout Realization
    Layout Gtk widgets on the screen during DOM realization.

    Scenario: Default Layout
        Given a UI DOM structure with a Window and 4 Buttons
        When the structure is realized
        Then the buttons should be laid out vertically

    Scenario: Grid Layout with default settings
        Given a UI DOM structure with a Window and 4 Buttons
        And the window layout is set to grid
        When the structure is realized
        Then the buttons should be laid out in the following positions:  
            | Button 0 | Button 1 |
            | Button 2 | Button 3 |

    Scenario: Grid Layout with custom size
        Given a UI DOM structure with a Window and 4 Buttons
        And the window layout is set to grid with size 3
        When the structure is realized
        Then the buttons should be laid out in the following positions:
            | Button 0 | Button 1 | Button 2 |
            | Button 3 |          |          |
