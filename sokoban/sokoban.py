import sys
import traceback
import copy
from sense_hat import SenseHat


class SokobanApp:
    MAP_WALL   = '#'
    MAP_FLOOR  = ' '
    MAP_GOAL   = '.'
    MAP_BOX    = '$'
    MAP_PLAYER = '@'

    COLOR_WALL    = (0, 0, 255)     # Blue
    COLOR_GOAL    = (255, 255, 0)   # Yellow
    COLOR_ON_GOAL = (0, 255, 0)     # Green
    COLOR_BOX     = (255, 0, 255)   # Purple
    COLOR_PLAYER  = (255, 255, 255) # White

    DIRECTION_MOVE_YX = {
        'up':    (-1,  0),
        'down':  ( 1,  0),
        'left':  ( 0, -1),
        'right': ( 0,  1),
    }

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
        self.show_map()
        self.show_player()

        try:
            status = 0
            prev_direction = None

            while status >= 0:
                for event in sense.stick.get_events():
                    if event.direction == prev_direction:
                        prev_direction = None
                        continue

                    move_yx = SokobanApp.DIRECTION_MOVE_YX.get(event.direction)
                    if move_yx:
                        self.move_player(move_yx[0], move_yx[1])

                        self.clear_display()
                        self.show_map()
                        self.show_player()

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

    def move_player(self, move_y, move_x):
        self.player_y += move_y
        self.player_x += move_x

        # TODO

    def clear_display(self):
        if not self.sense:
            return

        self.sense.clear()

    def show_player(self):
        if not self.sense:
            return

        self.sense.set_pixel(
            self.player_x, self.player_y, SokobanApp.COLOR_PLAYER)

    def show_map(self):
        if not self.sense:
            return

        for (y, cols) in enumerate(self.map):
            for (x, col) in enumerate(cols):
                if col == SokobanApp.MAP_WALL:
                    self.show_wall(y, x)

                elif col == SokobanApp.MAP_FLOOR:
                    pass

                elif col == SokobanApp.MAP_GOAL:
                    self.show_goal(y, x)

                elif col == SokobanApp.MAP_BOX:
                    self.show_box(y, x)

    def show_wall(self, y, x):
        self.sense.set_pixel(x, y, SokobanApp.COLOR_WALL)

    def show_goal(self, y, x):
        self.sense.set_pixel(x, y, SokobanApp.COLOR_GOAL)

    def show_box(self, y, x):
        self.sense.set_pixel(x, y, SokobanApp.COLOR_BOX)



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

