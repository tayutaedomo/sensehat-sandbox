import sys
import traceback
import copy
from sense_hat import SenseHat


class SokobanApp:
    MAP_WALL = '#'
    MAP_FLOOR = ' '
    MAP_GOAL = '.'
    MAP_BOX = '$'
    MAP_PLAYER = '@'

    def __init__(self, sense):
        self.sense = sense

        self.initialized = False
        self.map_original = []
        self.map = []
        self.player_y = None
        self.player_x = None

    def load_map(self, file_path):
        try:
            self.map_original = []
            self.map = []

            with open(file_path) as f:
                for line in f:
                    line = line.rstrip()
                    self.map_original.append(list(line))

            for (y, cols) in enumerate(self.map_original):
                row = []

                for (x, col) in enumerate(cols):
                    if col == SokobanApp.MAP_WALL:
                        row.append(col)
                    elif col == SokobanApp.MAP_FLOOR:
                        row.append(col)
                    elif col == SokobanApp.MAP_GOAL:
                        row.append(col)
                    elif col == SokobanApp.MAP_BOX:
                        row.append(col)
                    elif col == SokobanApp.MAP_PLAYER:
                        row.append(SokobanApp.MAP_FLOOR)
                        self.player_y = y
                        self.player_x = x

                self.map.append(row)

            self.initialized = True

            return self.initialized

        except Exception as e:
            #print(e)
            print(traceback.format_exc())

            return self.initialized

    def start(self):
        self.clear_display()
        self.show_player()

        try:
            status = 0
            prev_direction = None

            while status >= 0:
                for event in sense.stick.get_events():
                    if event.direction == prev_direction:
                        prev_direction = None
                        continue

                    #if event.direction == "up":
                    #if event.direction == "left":
                    #if event.direction == "down":
                    #if event.direction == "right":

                    if event.direction == "middle":
                        status = -1
                        sense.clear()

                    prev_direction = event.direction

            return True

        except KeyboardInterrupt:
            self.clear_display()
            return False

    def clear_display(self):
        if not self.sense:
            return

        self.sense.clear()

    def show_player(self):
        if not self.sense:
            return

        self.sense.set_pixel(
            self.player_x, self.player_y, (255, 255, 255))


if __name__ == '__main__':
    sense = SenseHat()
    app = SokobanApp(sense)

    if len(sys.argv) < 2:
        print('Map data path is required.')
        sys.exit()

    if not app.load_map(sys.argv[1]):
        print('Map data loading is failed.')
        sys.exit()

    app.start()

