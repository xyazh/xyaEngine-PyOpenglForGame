POS = 0b00000001
COL = 0b00000010
TEX = 0b00000100
NOR = 0b00001000
LIT = 0b00010000
SIZ = 0b00100000


class BufferBuilder:
    def __init__(self, pri_type: int, format_type: int):
        self.pri_type = pri_type
        self.format_type = format_type
        self.buffer = []
        self.temp_buffer = []
        self.offset_pos = 0
        self.offset_col = 0
        self.offset_tex = 0
        self.offset_nor = 0
        self.offset_lit = 0
        self.offset_siz = 0
        self.initTempBuffer()
        self.size = 0

    def initTempBuffer(self):
        count = 0
        if self.format_type & POS:
            self.offset_pos = count
            count += 3
        if self.format_type & COL:
            self.offset_col = count
            count += 4
        if self.format_type & TEX:
            self.offset_tex = count
            count += 2
        if self.format_type & NOR:
            self.offset_nor = count
            count += 3
        if self.format_type & LIT:
            self.offset_lit = count
            count += 2
        if self.format_type & SIZ:
            self.offset_siz = count
            count += 1
        self.temp_buffer = [0 for _ in range(count)]

    def pos(self, x: float | int, y: float | int, z: float | int):
        o = self.offset_pos
        self.temp_buffer[o] = x
        self.temp_buffer[o + 1] = y
        self.temp_buffer[o + 2] = z
        return self

    def col(self, r: float | int, g: float | int, b: float | int, a: float | int = 1):
        o = self.offset_col
        self.temp_buffer[o] = r
        self.temp_buffer[o + 1] = g
        self.temp_buffer[o + 2] = b
        self.temp_buffer[o + 3] = a
        return self

    def tex(self, u: float | int, v: float | int):
        o = self.offset_tex
        self.temp_buffer[o] = u
        self.temp_buffer[o + 1] = v
        return self
    def nor(self, x: float | int, y: float | int, z: float | int):
        o = self.offset_nor
        self.temp_buffer[o] = x
        self.temp_buffer[o + 1] = y
        self.temp_buffer[o + 2] = z
        return self

    def lit(self, u: float | int, v: float | int):
        o = self.offset_lit
        self.temp_buffer[o] = u
        self.temp_buffer[o + 1] = v
        return self
    
    def siz(self, s: float | int):
        o = self.offset_siz
        self.temp_buffer[o] = s
        return self

    def end(self):
        self.buffer += self.temp_buffer
        self.size += 1
