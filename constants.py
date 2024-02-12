# Do not delete unused imports
import os
import copy
import math
import time
from pprint import pprint
from typing import Any
from data_handler import DataHandler
import pygame as pg

VERSION = '1.0.0'


class GameStatus:
    INITIALISING = 0
    ADJUST_BRIGHTNESS = 1
    SPLASH_SCREEN = 2
    LOBBY = 3


class Colours:
    BG_COL = pg.Color(0, 5, 5)

    COL_GREY = pg.Color(2, 4, 2)
    BASE_COL_GREY = pg.Color(COL_GREY)

    COL_LIGHT_GREY = pg.Color(8, 10, 8)
    BASE_COL_LIGHT_GREY = pg.Color(COL_LIGHT_GREY)


def update_colours(data_handler: DataHandler):
    brightness = data_handler.get_option('brightness')
    col = pg.Color(brightness, brightness, brightness, 0)

    Colours.COL_GREY = Colours.BASE_COL_GREY + col
    Colours.COL_LIGHT_GREY = Colours.BASE_COL_LIGHT_GREY + col


LOGGING_FOLDER = 'files/logs/'
LEVELS_FOLDER = 'files/levels/'


UNIT = 18
WIDTH = 31
HEIGHT = 41
SCRN_WIDTH = UNIT * WIDTH
SCRN_HEIGHT = UNIT * HEIGHT
MARGIN = UNIT

EDITOR_SCRN_WIDTH = UNIT * WIDTH
EDITOR_SCRN_HEIGHT = UNIT * HEIGHT
