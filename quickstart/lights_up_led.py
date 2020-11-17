# Reference: https://note.com/agw/n/nc052420f3c37

from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.set_pixel(1, 2, [0, 0, 255])
sleep(2)
sense.clear()

