import os
import copy
import math
import time
from pprint import pprint
from typing import Any

import pygame as pg

BG_COL = pg.Color(0, 5, 5)

UNIT = 20
SCRN_WIDTH = UNIT * 31
SCRN_HEIGHT = UNIT * 41
MARGIN = UNIT
