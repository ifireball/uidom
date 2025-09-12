Feature: UI Button Realization
    Realize Buttons in UI DOM structures into Gtk widgets on screen.

    Scenario: Realize a Button
        Given a UI DOM structure with a Window and a Button with some random text
        When the structure is realized
        Then the Button should be visible in the Window
        And the Button should have the random text

    Scenario: Realize a Button with a click callback
        Given a UI DOM structure with a Window and a Button with a click callback
        When the structure is realized
        Then the Button should be visible in the Window
        When the Button is clicked
        Then the callback should be called
