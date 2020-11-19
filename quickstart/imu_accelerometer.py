#
# Reference: https://pythonhosted.org/sense-hat/api/#imu-sensor
#
import sys
import datetime
from sense_hat import SenseHat


def get_acceler_delta(current, prev):
    return {
        'x': current['x'] - prev['x'],
        'y': current['y'] - prev['y'],
        'z': current['z'] - prev['z'],
    }



if __name__ == '__main__':
    sense = SenseHat()
    sense.set_imu_config(False, False, True)  # Accelerometer only

    try:
        chFlg = 0
        prev_direction = None
        time_step = datetime.timedelta(milliseconds=250)

        while chFlg >= 0:
            for event in sense.stick.get_events():
                if event.direction == prev_direction:
                    prev_direction = None
                    continue

                if event.direction == "up":
                    accel_only = sense.get_accelerometer()
                    print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))
                    chFlg = 1

                if event.direction == "down":
                    raw = sense.get_accelerometer_raw()
                    print("x: {x}, y: {y}, z: {z}".format(**raw))
                    chFlg = 1

                if event.direction == "left":
                    chFlg = 2
                    start_time = datetime.datetime.now()
                    prev_raw = sense.get_accelerometer_raw()

                if event.direction == "right":
                    chFlg = 1

                if event.direction == "middle":
                    chFlg = -1

                prev_direction = event.direction

            if chFlg == 2 and datetime.datetime.now() > start_time + time_step:
                raw = sense.get_accelerometer_raw()
                #print("x: {x}, y: {y}, z: {z}".format(**raw))
                print("x: {x}, y: {y}, z: {z}".format(**(get_acceler_delta(raw, prev_raw))))
                prev_raw = raw

                start_time = datetime.datetime.now()

    except KeyboardInterrupt:
        sys.exit()

