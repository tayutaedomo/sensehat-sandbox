import os
import json
from time import sleep
from sense_hat import SenseHat


class Font4x8:
    def __init__(self):
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'font4x8.json')

        self.color_main = (255, 255, 255)
        self.color_shadow = (0, 0, 64)

        self.font_char = {}
        self.init_font()

    def init_font(self):
        with open(self.json_path) as f:
            self.font_char = json.load(f)

    def show_chars(self, chars):
        if len(chars) == 1:
            self.show_char(chars[0], True, False)
        else:
            self.show_char(chars[0], True, False)
            self.show_char(chars[1], False, True)

    def show_char(self, char, clear=False, right=True):
        font_data = self.font_char.get(char)

        if not font_data:
            return

        sense = SenseHat()

        if clear:
            sense.clear()

        for (y, row) in enumerate(font_data):
            start = 4 if right else 0

            for (x, cell) in enumerate(row, start):
                if cell == 1:
                    sense.set_pixel(x, y, self.color_main)
                elif cell == 2:
                    sense.set_pixel(x, y, self.color_shadow)


class Char4x8:
    UPPER_CHARS = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    LOWER_CHARS = [
        '0s', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    SYMBOLS = [
        '.', ',', '-', '+', 'div', '*', '=', '/', '\'', '"', '!',
        '?', ':', 'deg', '_', 'box', '(', ')', '[2', ']2', '[', ']'
    ]

    def __init__(self):
        self.index_u = -1
        self.index_l = -1
        self.index_s = -1

    def next_upper_char(self):
        self.index_u += 1
        if len(Char4x8.UPPER_CHARS) <= self.index_u:
            self.index_u = 0
        return Char4x8.UPPER_CHARS[self.index_u]

    def next_lower_char(self):
        self.index_l += 1
        if len(Char4x8.LOWER_CHARS) <= self.index_l:
            self.index_l = 0
        return Char4x8.LOWER_CHARS[self.index_l]

    def next_symbol(self):
        self.index_s += 1
        if len(Char4x8.SYMBOLS) <= self.index_s:
            self.index_s = 0
        return Char4x8.SYMBOLS[self.index_s]


if __name__ == '__main__':
    font = Font4x8()

    sense = SenseHat()
    sense.clear()

    chFlg = 0
    char = Char4x8()
    prev_direction = None

    while chFlg >= 0:
        for event in sense.stick.get_events():
            if event.direction == prev_direction:
                prev_direction = None
                continue

            if event.direction == "down":
                chFlg = 1
                font.show_char(char.next_upper_char(), True, False)
                font.show_char(char.next_upper_char(), False, True)

            if event.direction == "up":
                chFlg = 1
                font.show_chars([char.next_lower_char(), char.next_lower_char()])

            #if event.direction == "right":
            #    chFlg = 1

            if event.direction == "left":
                chFlg = 1
                font.show_chars([char.next_symbol()])

            if event.direction == "middle":
                chFlg = -1
                sense.clear()

            prev_direction = event.direction

