#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: https://www.itmedia.co.jp/news/articles/2010/09/news015.html

from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

try:
    while True:
        sense.show_letter("L", red)
        sleep(1)
        sense.show_letter("a", blue)
        sleep(1)
        sense.show_letter("u", green)
        sleep(1)
        sense.show_letter("r", white)
        sleep(1)
        sense.show_letter("a", yellow)
        sleep(1)
except KeyboardInterrupt:
    sense.clear()

