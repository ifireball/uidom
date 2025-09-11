Feature: UI Button Realization
    Realize Buttons in UI DOM structures into Gtk widgets on screen.

    Scenario: Realize a Button
        Given a UI DOM structure with a Window and a Button
        When the structure is realized
        Then the Button should be visible in the Window
