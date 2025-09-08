Feature: UI DOM Realization
    Realize UI DOM structures into Gtk widgets on screen.

    Scenario: Realize a Window
        Given a UI DOM structure with a Window
        When the structure is realized
        Then the Window should be visible on screen

