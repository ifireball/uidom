from math import ceil, floor

def center(text: str, width: int, fill: str = " ") -> str:
    """
    Center the text in the width with the fill character.

    >>> center("Hello", 10)
    '   Hello  '
    >>> center("Hello", 10, "*")
    '***Hello**'
    >>> center("Hello", 11, "*")
    '***Hello***'
    """
    return f"{fill * ceil((width - len(text)) / 2)}{text}{fill * floor((width - len(text)) / 2)}"
