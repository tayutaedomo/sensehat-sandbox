#
# Reference: https://pythonhosted.org/sense-hat/api/#imu-sensor
#
import sys
from sense_hat import SenseHat


if __name__ == '__main__':
    sense = SenseHat()
    sense.set_imu_config(False, True, False)  # Gyroscope only

    try:
        chFlg = 0
        prev_direction = None

        while chFlg >= 0:
            for event in sense.stick.get_events():
                if event.direction == prev_direction:
                    prev_direction = None
                    continue

                if event.direction == "up":
                    gyro_only = sense.get_gyroscope()
                    print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))

                if event.direction == "down":
                    raw = sense.get_gyroscope_raw()
                    print("x: {x}, y: {y}, z: {z}".format(**raw))

                #if event.direction == "right":
                #if event.direction == "left":

                if event.direction == "middle":
                    chFlg = -1

                prev_direction = event.direction

    except KeyboardInterrupt:
        sys.exit()

