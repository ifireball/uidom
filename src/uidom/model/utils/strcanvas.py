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
        left, top, right, bottom = x, y, x + width - 1, y + height - 1
        self._blit_row(left, top, border[0:1])
        self._blit_row(left+1, top, border[1:2] * (width - 2))
        self._blit_row(right, top, border[2:3])
        self._blit_column(right, top+1, border[3:4] * (height - 2))
        self._blit_row(right, bottom, border[4:5])
        self._blit_row(left+1, bottom, border[5:6] * (width - 2))
        self._blit_row(left, bottom, border[6:7])
        self._blit_column(left, top+1, border[7:8] * (height - 2))
        return self

    def draw_text(self, x: int, y: int, text: str) -> StrCanvas:
        r'''
        Draw the text at the given position.
        >>> str(StrCanvas(width=10, height=4, fill="*").draw_text(1, 1, "Hello"))
        '**********\n*Hello****\n**********\n**********'
        '''
        self._blit_row(x, y, text.encode('ascii', 'replace'))
        return self

    def _blit_row(self, x: int, y: int, row: bytes|bytearray|memoryview) -> StrCanvas:
        self.canvas[y*self.width+x:y*self.width+x+len(row)] = row
        return self

    def _blit_column(self, x: int, y: int, column: bytes|bytearray|memoryview) -> StrCanvas:
        if y >= self.height:
            return self
        self.canvas[y*self.width+x:(y+len(column))*self.width+x:self.width] = column[0:min(len(column), self.height - y)]
        return self
