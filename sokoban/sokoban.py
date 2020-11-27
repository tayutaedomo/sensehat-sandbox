import sys
import traceback
import copy
from datetime import datetime, timedelta
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
        self.map = []
        self.map_height = 0
        self.map_width = 0
        self.floor = Floor(self, SokobanApp.COLOR_WALL, SokobanApp.COLOR_GOAL)
        self.player = Player(self, SokobanApp.COLOR_PLAYER)
        self.box_manager = BoxManager(self)

    def load_map(self, file_path):
        try:
            self.map = []

            with open(file_path) as f:
                for line in f:
                    line = line.rstrip()
                    self.map.append(list(line))

            for (y, cols) in enumerate(self.map):
                for (x, col) in enumerate(cols):
                    if col == SokobanApp.MAP_BOX:
                        self.box_manager.new_box(y, x)

                    elif col == SokobanApp.MAP_PLAYER:
                        self.player.init(y, x)

            if len(self.map) > 1:
                self.map_height = len(self.map)
                self.map_width = len(self.map[0])

            self.initialized = True

            return self.initialized

        except Exception as e:
            #print(e)
            print(traceback.format_exc())

            return self.initialized

    def start(self):
        self.clear_display()
        self.floor.show(True)
        self.box_manager.show()

        try:
            status = 0
            prev_direction = None

            while status >= 0:
                self.player.show()

                for event in sense.stick.get_events():
                    if event.direction == prev_direction:
                        prev_direction = None
                        continue

                    prev_direction = event.direction

                    move_yx = SokobanApp.DIRECTION_MOVE_YX.get(event.direction)

                    if move_yx:
                        self.player.move(move_yx[0], move_yx[1])

                        self.floor.show()
                        self.box_manager.show()
                        self.player.show()

                        if self.box_manager.is_all_on_goal():
                            print('CLEAR!')
                            self.show_clear()
                            status = -1

                    if event.direction == "middle":
                        status = -1
                        sense.clear()

            return True

        except KeyboardInterrupt:
            self.clear_display()
            return False

    def clear_display(self):
        if not self.sense:
            return

        self.sense.clear()

    def show_clear(self):
        self.sense.show_message('CLEAR!')

    def get_map_cell(self, y, x):
        return self.map[y][x]


class Floor:
    def __init__(self, app, color_wall, color_goal):
        self.app = app
        self.color_wall = color_wall
        self.color_goal = color_goal

    def show(self, wall=False):
        if not self.app.sense:
            return

        if wall:
            self.show_walls()

        self.show_goals()

    def show_walls(self):
        for y in range(self.app.map_height):
            for x in range(self.app.map_width):
                cell = self.app.get_map_cell(y, x)

                if cell == SokobanApp.MAP_WALL:
                    self.show_wall(y, x)

    def show_wall(self, y, x):
        self.app.sense.set_pixel(x, y, self.color_wall)

    def show_goals(self):
        for y in range(self.app.map_height):
            for x in range(self.app.map_width):
                cell = self.app.get_map_cell(y, x)

                if cell == SokobanApp.MAP_GOAL:
                    self.show_goal(y, x)

    def show_goal(self, y, x):
        self.app.sense.set_pixel(x, y, self.color_goal)


class Player:
    def __init__(self, app, color):
        self.app = app
        self.color = color
        self.led = LedFlash(self, 200)

    def init(self, y, x):
        self.y = y
        self.x = x

    def show(self):
        if not self.app.sense:
            return

        self.led.flash()

    def light(self):
        if not self.app.sense:
            return

        self.app.sense.set_pixel(self.x, self.y, self.color)

    def light_off(self):
        if not self.app.sense:
            return

        self.app.sense.set_pixel(self.x, self.y, (0, 0, 0))

    def move(self, move_y, move_x):
        next_y = self.y + move_y
        next_x = self.x + move_x

        next_cell = self.app.get_map_cell(next_y, next_x)

        if next_cell == SokobanApp.MAP_WALL:
            return

        ret_box_move = self.app.box_manager.move(next_y, next_x, move_y, move_x)

        if ret_box_move == False:
            return

        self.light_off()

        self.y = next_y
        self.x = next_x


class LedFlash:
    def __init__(self, led, interval=0):
        self.led = led

        self.is_light_on = False
        self.interval_td = timedelta(milliseconds=interval)
        self.start_time = None

    def light(self):
        self.led.light()

        if not self.is_light_on:
            self.is_light_on = True
            self.start_time = datetime.now()

    def light_off(self):
        self.led.light_off()

        if self.is_light_on:
            self.is_light_on = False
            self.start_time = datetime.now()

    def flash(self):
        if self.start_time is None:
            self.is_light_on = True
            self.start_time = datetime.now()

        if datetime.now() > self.start_time + self.interval_td:
            self.is_light_on = not self.is_light_on
            self.start_time = datetime.now()

        if self.is_light_on:
            self.light()
        else:
            self.light_off()


class BoxManager:
    def __init__(self, app):
        self.app = app
        self.boxes = []

    def new_box(self, y, x):
        box = Box(app, y, x)
        self.boxes.append(box)

    def show(self):
        if not self.app.sense:
            return

        for box in self.boxes:
            box.show()

    def move(self, y, x, move_y, move_x):
        for box in self.boxes:
            ret_move = box.move(y, x, move_y, move_x)

            if ret_move is not None:
                return ret_move

        return None

    def is_box_collision(self, y, x):
        for box in self.boxes:
            if box.is_collision(y, x):
                return True

        return False

    def is_all_on_goal(self):
        ret = True

        for box in self.boxes:
            if not box.is_on_goal():
                ret = False

        return ret


class Box:
    def __init__(self, app, y, x):
        self.app = app
        self.y = y
        self.x = x

    def show(self):
        if self.is_on_goal():
            self.show_on_goal()
        else:
            self.show_box()

    def show_box(self):
        self.app.sense.set_pixel(self.x, self.y, SokobanApp.COLOR_BOX)

    def show_on_goal(self):
        self.app.sense.set_pixel(self.x, self.y, SokobanApp.COLOR_ON_GOAL)

    def move(self, y, x, move_y, move_x):
        if not self.is_collision(y, x):
            return None

        next_y = y + move_y
        next_x = x + move_x

        next_cell = self.app.get_map_cell(next_y, next_x)

        if next_cell == SokobanApp.MAP_WALL:
            return False

        is_collision = self.app.box_manager.is_box_collision(next_y, next_x)

        if is_collision:
            return False

        self.y = next_y
        self.x = next_x

        return True

    def is_collision(self, y, x):
        return y == self.y and x == self.x

    def is_on_goal(self):
        return self.app.get_map_cell(self.y, self.x) == SokobanApp.MAP_GOAL



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

