import os
import copy
import math
import time
from pprint import pprint
from typing import Any

import pygame as pg

VERSION = '1.0.0'

BG_COL = pg.Color(0, 5, 5)

UNIT = 18
WIDTH = 31
HEIGHT = 41
SCRN_WIDTH = UNIT * WIDTH
SCRN_HEIGHT = UNIT * HEIGHT
MARGIN = UNIT

COL_GREY = pg.Color(12, 14, 12)
COL_LIGHT_GREY = pg.Color(18, 20, 18)
