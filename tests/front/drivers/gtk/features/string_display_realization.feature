Feature: UI String Display Widget Realization

    Realize String Display widgets in UI DOM structures into Gtk widgets on screen.

    Scenario: Realize a String Display
        Given a UI DOM structure with a Window and a String Display with some random text
        When the structure is realized
        Then the String Display should be visible in the Window as a Gtk.Label
        And the String Display should have the random text
