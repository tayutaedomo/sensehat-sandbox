import sys
from datetime import datetime, timedelta
from sense_hat import SenseHat


class LedFlash:
    def __init__(self, sense, interval=0):
        self.sense = sense
        self.color = (255, 255, 255)
        self.x = 1
        self.y = 2

        self.is_light_on = False
        self.interval_td = timedelta(milliseconds=interval)
        self.start_time = None

    def light(self):
        self.sense.set_pixel(self.x, self.y, self.color)

        if not self.is_light_on:
            self.is_light_on = True
            self.start_time = datetime.now()

    def light_off(self):
        self.sense.set_pixel(self.x, self.y, (0, 0, 0))

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



if __name__ == '__main__':
    sense = SenseHat()
    led = LedFlash(sense, 500)

    try:
        chFlg = 0
        prev_direction = None

        while chFlg >= 0:
            led.flash()

            for event in sense.stick.get_events():
                if event.direction == prev_direction:
                    prev_direction = None
                    continue

                prev_direction = event.direction

                #if event.direction == "up":
                #if event.direction == "left":
                #if event.direction == "down":
                #if event.direction == "right":

                if event.direction == "middle":
                    chFlg = -1
                    sense.clear()

    except KeyboardInterrupt:
        sense.clear()
        sys.exit()

