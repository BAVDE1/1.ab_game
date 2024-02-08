import os
import copy
import math
import time
from pprint import pprint
from typing import Any
from save_handler import SaveHandler
import pygame as pg

VERSION = '1.0.0'


class GameStatus:
    ADJUST_BRIGHTNESS = 1
    SPLASH_SCREEN = 2
    LOBBY = 3


class Colours:
    COL_GREY = pg.Color(2, 4, 2)
    BASE_COL_GREY = pg.Color(COL_GREY)

    COL_LIGHT_GREY = pg.Color(8, 10, 8)
    BASE_COL_LIGHT_GREY = pg.Color(COL_LIGHT_GREY)


def update_colours(save_handler: SaveHandler):
    brightness = save_handler.get_option('brightness')
    col = pg.Color(brightness, brightness, brightness, 0)

    Colours.COL_GREY = Colours.BASE_COL_GREY + col
    Colours.COL_LIGHT_GREY = Colours.BASE_COL_LIGHT_GREY + col


BG_COL = pg.Color(0, 5, 5)

UNIT = 18
WIDTH = 31
HEIGHT = 41
SCRN_WIDTH = UNIT * WIDTH
SCRN_HEIGHT = UNIT * HEIGHT
MARGIN = UNIT
