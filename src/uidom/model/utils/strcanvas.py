from __future__ import annotations

class StrCanvas:
    r'''
    A canvas of bytes that supports drawing borders and text and can be converted
    to a multi-line string.

    >>> str(StrCanvas(width=10, height=4, fill="*"))
    '**********\n**********\n**********\n**********'
    '''
    def __init__(self, width: int, height: int, fill: str = " "):
        self.width = width
        self.height = height
        self.canvas = bytearray(fill.encode('ascii', 'replace')) * width * height

    def __str__(self):
        lines = (self.canvas[i:i+self.width].decode('ascii', 'replace') for i in range(0, len(self.canvas), self.width))
        return "\n".join(lines)

    def draw_border(self, x: int, y: int, width: int, height: int, border: bytes = b'+-+|+-+|') -> StrCanvas:
        r'''
        Draw a border with the given width and height at the given position.
        the 'border' argument should contain 8 bytes indicating the top-left, top, top-right, right, bottom-right, bottom, bottom-left, left bytes to use.

        >>> str(StrCanvas(width=10, height=4, fill="*").draw_border(0, 0, 10, 4))
        '+--------+\n|********|\n|********|\n+--------+'
        >>> str(StrCanvas(width=10, height=4, fill="*").draw_border(1, 1, 6, 3, border=b'ABCDEFGH'))
        '**********\n*ABBBBC***\n*H****D***\n*GFFFFE***'
        '''
        self.canvas[y*self.width+x] = border[0]
        self.canvas[y*self.width+x+1:y*self.width+x+width-1] = border[1:2] * (width - 2)
        self.canvas[y*self.width+x+width-1] = border[2]
        self.canvas[(y+1)*self.width+x+width-1:(y+height-1)*self.width+x+width-1:self.width] = border[3:4] * (height - 2)
        self.canvas[(y+height-1)*self.width+x+width-1] = border[4]
        self.canvas[(y+height-1)*self.width+x+1:(y+height-1)*self.width+x+width-1] = border[5:6] * (width - 2)
        self.canvas[(y+height-1)*self.width+x] = border[6]
        self.canvas[(y+1)*self.width+x:(y+height-1)*self.width+x:self.width] = border[7:8] * (height - 2)
        return self

    def draw_text(self, x: int, y: int, text: str) -> StrCanvas:
        r'''
        Draw the text at the given position.
        >>> str(StrCanvas(width=10, height=4, fill="*").draw_text(1, 1, "Hello"))
        '**********\n*Hello****\n**********\n**********'
        '''
        self.canvas[y*self.width+x:y*self.width+x+len(text)] = text.encode('ascii', 'replace')
        return self
