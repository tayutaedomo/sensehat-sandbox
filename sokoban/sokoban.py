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
        self.map_origin = []
        self.map = []
        self.player = None
        self.box_manager = None

    def load_map(self, file_path):
        try:
            self.map_origin = []
            self.map = []

            with open(file_path) as f:
                for line in f:
                    line = line.rstrip()
                    self.map_origin.append(list(line))

            for (y, cols) in enumerate(self.map_origin):
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
                        self.player = Player(self, y, x)

                self.map.append(row)

            self.box_manager = BoxManager(self)

            self.initialized = True

            return self.initialized

        except Exception as e:
            #print(e)
            print(traceback.format_exc())

            return self.initialized

    def start(self):
        self.clear_display()
        self.show_map()
        self.box_manager.show()
        self.player.show()

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
                        self.player.move(move_yx[0], move_yx[1])

                        self.clear_display()
                        self.show_map()
                        self.box_manager.show()
                        self.player.show()

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

    def show_map(self):
        if not self.sense:
            return

        for (y, cols) in enumerate(self.map_origin):
            for (x, col) in enumerate(cols):
                if col == SokobanApp.MAP_WALL:
                    self.show_wall(y, x)

                elif col == SokobanApp.MAP_FLOOR:
                    pass

                elif col == SokobanApp.MAP_GOAL:
                    self.show_goal(y, x)

    def show_wall(self, y, x):
        self.sense.set_pixel(x, y, SokobanApp.COLOR_WALL)

    def show_goal(self, y, x):
        self.sense.set_pixel(x, y, SokobanApp.COLOR_GOAL)


class Player:
    def __init__(self, app, y, x):
        self.app = app
        self.y = y
        self.x = x

    def show(self):
        if not self.app.sense:
            return

        self.app.sense.set_pixel(self.x, self.y, SokobanApp.COLOR_PLAYER)

    def move(self, move_y, move_x):
        next_y = self.y + move_y
        next_x = self.x + move_x

        next_cell = self.app.map[next_y][next_x]

        if next_cell == SokobanApp.MAP_WALL:
            return

        ret_box_move = self.app.box_manager.move(next_y, next_x, move_y, move_x)

        if ret_box_move == False:
            return

        self.y = next_y
        self.x = next_x


class BoxManager:
    def __init__(self, app):
        self.app = app

    def show(self):
        if not self.app.sense:
            return

        for (y, cols) in enumerate(self.app.map):
            for (x, col) in enumerate(cols):
                if col == SokobanApp.MAP_BOX:
                    self.show_box(y, x)

                # TODO: On goal case
                #elif col == SokobanApp.MAP_GOAL:
                #    self.show_goal(y, x)

    def show_box(self, y, x):
        self.app.sense.set_pixel(x, y, SokobanApp.COLOR_BOX)

    def move(self, y, x, move_y, move_x):
        cell = self.app.map[y][x]

        if cell != SokobanApp.MAP_BOX:
            return None

        next_y = y + move_y
        next_x = x + move_x
        next_cell = self.app.map[next_y][next_x]

        if next_cell == SokobanApp.MAP_WALL:
            return False

        elif next_cell == SokobanApp.MAP_BOX:
            return False

        self.app.map[y][x] = SokobanApp.MAP_FLOOR
        self.app.map[next_y][next_x] = SokobanApp.MAP_BOX

        return True



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

