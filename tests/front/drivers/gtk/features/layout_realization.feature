Feature: UI Layout Realization
    Layout Gtk widgets on the screen during DOM realization.

    Scenario: Default Layout
        Given a UI DOM structure with a Window and 4 Buttons
        When the structure is realized
        Then the buttons should be laid out vertically
