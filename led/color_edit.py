from sense_hat import SenseHat
from time import sleep


class ColorEditor:
    MAX_RED   = 255
    MAX_GREEN = 255
    MAX_BLUE  = 255

    def __init__(self, step=64):
        self.step = step

        self.red = 0
        self.green = 0
        self.blue = 0

    def get_color(self):
        color = (self.red, self.green, self.blue)
        print(color)
        return color

    def next_red(self):
        self.red += self.step

        if self.red > ColorEditor.MAX_RED:
            self.red -= (ColorEditor.MAX_RED + 1)

        return self.get_color()

    def next_green(self):
        self.green += self.step

        if self.green > ColorEditor.MAX_GREEN:
            self.green -= (ColorEditor.MAX_GREEN + 1)

        return self.get_color()

    def next_blue(self):
        self.blue += self.step

        if self.blue > ColorEditor.MAX_BLUE:
            self.blue -= (ColorEditor.MAX_BLUE + 1)

        return self.get_color()



if __name__ == '__main__':
    sense = SenseHat()
    sense.clear()

    editor = ColorEditor()
    color = editor.get_color()

    chFlg = 0
    prev_direction = None

    while chFlg >= 0:
        for event in sense.stick.get_events():
            if event.direction == prev_direction:
                prev_direction = None
                continue

            if event.direction == 'up':
                chFlg = 1
                color = editor.next_red()

            if event.direction == 'left':
                chFlg = 1
                color = editor.next_green()

            if event.direction == 'down':
                chFlg = 1
                color = editor.next_blue()

            #if event.direction == 'right':
            #    chFlg = 1

            if event.direction in ['up', 'left', 'down', 'right']:
                #sense.clear()
                sense.show_letter('#', color)

            if event.direction == 'middle':
                chFlg = -1
                sense.clear()

            prev_direction = event.direction

