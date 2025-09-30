Feature: Print Window Layout
    Print the layout of a window.

    Scenario: Print the layout of a window with a button when the button sets the size
        Given a button with the following text
            """
            Some button
            """
        And it is embedded in a window with the following title
            """
            Window 1
            """
        When the layout is printed
        Then the following layout should be printed
            """
            #### Window 1 ###
            #/-------------\#
            #| Some button |#
            #\-------------/#
            #################
            """

    Scenario: Print the layout of a window with a button when the title sets the size
        Given a button with the following text
            """
            Button 1
            """
        And it is embedded in a window with the following title
            """
            Window with a long title
            """
        When the layout is printed
        Then the following layout should be printed
            """
            ## Window with a long title ##
            #/--------------------------\#
            #|         Button 1         |#
            #\--------------------------/#
            ##############################
            """
