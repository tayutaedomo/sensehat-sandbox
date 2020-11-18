#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: https://www.itmedia.co.jp/news/articles/2010/09/news015.html

from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()


# Generate a random colour
def pick_random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)


try:
  while True:
    sense.show_letter("L", pick_random_colour())
    sleep(1)
    sense.show_letter("a", pick_random_colour())
    sleep(1)
    sense.show_letter("u", pick_random_colour())
    sleep(1)
    sense.show_letter("r", pick_random_colour())
    sleep(1)
    sense.show_letter("a", pick_random_colour())
    sleep(1)
except KeyboardInterrupt:
    sense.clear()

