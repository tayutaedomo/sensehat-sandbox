import os
import json
from time import sleep
from sense_hat import SenseHat


class Font8x8:
    def __init__(self):
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'font8x8.json')

        self.color_main = (255, 255, 255)
        self.color_shadow = (0, 0, 64)

        self.font_char = {}
        self.init_font()

    def init_font(self):
        with open(self.json_path) as f:
            self.font_char = json.load(f)

    def show_char(self, char):
        font_data = self.font_char.get(char)

        if not font_data:
            return

        sense = SenseHat()
        sense.clear()

        for (y, row) in enumerate(font_data):
            for (x, cell) in enumerate(row):
                if cell == 1:
                    sense.set_pixel(x, y, self.color_main)
                elif cell == 2:
                    sense.set_pixel(x, y, self.color_shadow)


class Char8x8:
    NUMERICS = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ]
    UPPER_CHARS = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    LOWER_CHARS = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    SYMBOLS = [
        '.', ',', '-', '+', 'div', '*', '=', '/', '**', '\'', '"', '`', '!',
        '?', ':', '&', '(', ')', '[', ']', '_', '#', 'deg', 'box'
    ]

    def __init__(self):
        self.index_n = -1
        self.index_u = -1
        self.index_l = -1
        self.index_s = -1

    def next_numeric(self):
        self.index_n += 1
        if self.index_n >= len(Char8x8.NUMERICS):
            self.index_n = 0
        return Char8x8.NUMERICS[self.index_n]

    def next_upper_char(self):
        self.index_u += 1
        if self.index_u >= len(Char8x8.UPPER_CHARS):
            self.index_u = 0
        return Char8x8.UPPER_CHARS[self.index_u]

    def next_lower_char(self):
        self.index_l += 1
        if self.index_l >= len(Char8x8.LOWER_CHARS):
            self.index_l = 0
        return Char8x8.LOWER_CHARS[self.index_l]

    def next_symbol(self):
        self.index_s += 1
        if self.index_s >= len(Char8x8.SYMBOLS):
            self.index_s = 0
        return Char8x8.SYMBOLS[self.index_s]



if __name__ == '__main__':
    font8x8 = Font8x8()

    sense = SenseHat()
    sense.clear()

    chFlg = 0
    char8x8 = Char8x8()
    prev_direction = None

    while chFlg >= 0:
        for event in sense.stick.get_events():
            if event.direction == prev_direction:
                prev_direction = None
                continue

            if event.direction == "down":
                chFlg = 1
                font8x8.show_char(char8x8.next_numeric())

            if event.direction == "up":
                chFlg = 1
                font8x8.show_char(char8x8.next_upper_char())

            if event.direction == "right":
                chFlg = 1
                font8x8.show_char(char8x8.next_lower_char())

            if event.direction == "left":
                chFlg = 1
                font8x8.show_char(char8x8.next_symbol())

            if event.direction == "middle":
                chFlg = -1
                sense.clear()

            prev_direction = event.direction

