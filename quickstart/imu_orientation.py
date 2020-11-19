#
# Reference: https://pythonhosted.org/sense-hat/api/#imu-sensor
#
import sys
from sense_hat import SenseHat


if __name__ == '__main__':
    sense = SenseHat()

    try:
        chFlg = 0
        prev_direction = None

        while chFlg >= 0:
            for event in sense.stick.get_events():
                if event.direction == prev_direction:
                    prev_direction = None
                    continue

                if event.direction == "down":
                    orientation_rad = sense.get_orientation_radians()
                    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))

                if event.direction == "up":
                    orientation = sense.get_orientation_degrees()
                    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

                #if event.direction == "right":
                #if event.direction == "left":

                if event.direction == "middle":
                    chFlg = -1

                prev_direction = event.direction

    except KeyboardInterrupt:
        sys.exit()

