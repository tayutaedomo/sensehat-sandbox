#
# Reference: https://pythonhosted.org/sense-hat/api/#imu-sensor
#
import sys
from sense_hat import SenseHat


if __name__ == '__main__':
    sense = SenseHat()
    sense.set_imu_config(True, False, False)  # Compass only

    try:
        chFlg = 0
        prev_direction = None

        while chFlg >= 0:
            for event in sense.stick.get_events():
                if event.direction == prev_direction:
                    prev_direction = None
                    continue

                if event.direction == "up":
                    north = sense.get_compass()
                    print("North: %s" % north)

                if event.direction == "down":
                    raw = sense.get_compass_raw()
                    print("x: {x}, y: {y}, z: {z}".format(**raw))

                #if event.direction == "right":
                #if event.direction == "left":

                if event.direction == "middle":
                    chFlg = -1

                prev_direction = event.direction

    except KeyboardInterrupt:
        sys.exit()

