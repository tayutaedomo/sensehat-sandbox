#
# Reference: https://pythonhosted.org/sense-hat/api/#imu-sensor
#
import sys
import datetime
from sense_hat import SenseHat


if __name__ == '__main__':
    sense = SenseHat()
    sense.set_imu_config(False, True, False)  # Gyroscope only

    try:
        chFlg = 0
        prev_direction = None
        time_step = datetime.timedelta(milliseconds=250)

        while chFlg >= 0:
            for event in sense.stick.get_events():
                if event.direction == prev_direction:
                    prev_direction = None
                    continue

                if event.direction == 'up':
                    chFlg = 1
                    gyro_only = sense.get_gyroscope()
                    print('p: {pitch}, r: {roll}, y: {yaw}'.format(**gyro_only))

                if event.direction == 'down':
                    chFlg = 2
                    raw = sense.get_gyroscope_raw()
                    print('x: {x}, y: {y}, z: {z}'.format(**raw))

                if event.direction == 'left':
                    chFlg += 10
                    start_time = datetime.datetime.now()

                if event.direction == 'right':
                    chFlg = 0

                if event.direction == 'middle':
                    chFlg = -1

                prev_direction = event.direction

            if chFlg > 2 and datetime.datetime.now() > start_time + time_step:
                if chFlg % 2 == 1:
                    gyro_only = sense.get_gyroscope()
                    print('p: {pitch}, r: {roll}, y: {yaw}'.format(**gyro_only))

                elif chFlg % 2 == 0:
                    raw = sense.get_gyroscope_raw()
                    print('x: {x}, y: {y}, z: {z}'.format(**raw))

                start_time = datetime.datetime.now()

    except KeyboardInterrupt:
        sys.exit()

