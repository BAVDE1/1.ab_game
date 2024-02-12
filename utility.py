from constants import *
from datetime import datetime
import logging


def get_logger(log_name_override="%Y-%m-%d (%H;%M.%S)"):
    log_file = f'{LOGGING_FOLDER}{datetime.now().strftime(log_name_override)}.log'
    if not os.path.exists(LOGGING_FOLDER):
        os.makedirs(LOGGING_FOLDER)
    files = os.listdir(LOGGING_FOLDER)
    if len(files) > 10:
        os.remove(f'{LOGGING_FOLDER}{files[0]}')
    logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)-8s :: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    logging.debug('created logger successfully')
    return logging.getLogger(__name__)


def parse_level_file(level_name):
    file_name = LEVELS_FOLDER + level_name.split('.')[0] + '.txt'
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f'Cannot find file {file_name}')

    with open(file_name) as fh:
        return fh.read().split('\n')


def enumerate_function(lines: list[str]):
    """
    Calls function for each `character` of each `string` in the given list (matrix), returning `x` and `y` accordingly\n
    Function must have params `x`, `y`, and `char`
    """
    def enum_func(func):
        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                func(x, y, char)
    return enum_func


def get_pos_from_relative(rel_pos: pg.Vector2) -> pg.Vector2:
    return pg.Vector2((rel_pos.x * UNIT) + MARGIN, (rel_pos.y * UNIT) + MARGIN)


def get_relative_from_pos(pos: pg.Vector2) -> pg.Vector2:
    return pg.Vector2((pos.x - MARGIN) / UNIT, (pos.y - MARGIN) / UNIT)
