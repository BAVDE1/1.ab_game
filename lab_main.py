import os.path
import random
import logging
import time
from datetime import datetime

from blocks import BaseBlock, FancyBlock, PlatformBlock, GreyBlock, LightGreyBlock, OutlineBlock, LogoBlock, WaveBlock
from constants import *
from data_handler import SaveHandler


LOGGING_FOLDER = 'files/logs/'
LEVELS_FOLDER = 'files/levels/'

CHAR_TO_BLOCK = {
    '#': BaseBlock,
    '*': FancyBlock,
    '-': PlatformBlock,

    ':': LightGreyBlock,
    '.': GreyBlock,
}
OUTLINE_CHARS = ['#', '*', '-']


def get_logger():
    log_file = f'{LOGGING_FOLDER}{datetime.now().strftime("%Y-%m-%d (%H;%M.%S)")}.log'
    if not os.path.exists(LOGGING_FOLDER):
        os.makedirs(LOGGING_FOLDER)
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


class Cover:
    def __init__(self):
        self.pos: pg.Vector2 = pg.Vector2(0, SCRN_HEIGHT / 2)
        self.cover_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.outline_group: pg.sprite.Group = pg.sprite.Group()

        # generates a bunch of random positions
        self.bulge_positions = [pg.Vector2(random.randrange(0, SCRN_WIDTH), random.randrange(0, SCRN_HEIGHT)) for _ in range(4)]

    def add_outline_sprite(self, sprite: pg.sprite.Sprite):
        sprite.add(self.outline_group)

    def empty(self):
        self.outline_group.empty()

    def update_outline(self):
        # update bulge positions first
        for index, pos in enumerate(self.bulge_positions):
            i = index + 2
            amp = UNIT * (0.05 * i)
            sine_time = time.time() - (10 * i)
            self.bulge_positions[index] = pg.Vector2(pos.x + (amp * math.sin(sine_time + 10)), pos.y + (amp * math.sin(sine_time - 10)))
        self.outline_group.update(bulge_positions=self.bulge_positions, cover_pos=self.pos)

    def draw(self, canvas_screen: pg.Surface):
        self.update_outline()

        self.cover_surface.fill(BG_COL)
        self.outline_group.draw(self.cover_surface)
        # for pos in self.bulge_positions:
        #     pg.draw.rect(self.cover_surface, (255, 0, 0), pg.Rect(pos.x - self.pos.x, pos.y - self.pos.y, 5, 5))

        canvas_screen.blit(self.cover_surface, self.pos)


class Wave:
    def __init__(self):
        self.pos: pg.Vector2 = pg.Vector2()

        self.wave_group: pg.sprite.Group = pg.sprite.Group()
        self.wave_group.add(*[WaveBlock(pg.Vector2(x * UNIT, 0), x) for x in range(WIDTH)])

    def update(self, cover):
        self.wave_group.update(y_pos=cover.pos.y)

    def draw(self, canvas_screen: pg.Surface, cover: Cover):
        self.update(cover)
        self.wave_group.draw(canvas_screen)


class Logo:
    def __init__(self):
        self.pos: pg.Vector2 = pg.Vector2()
        self.group: pg.sprite.Group = pg.sprite.Group()

    def create_logo(self):
        with open('files/logo.txt') as fh:
            parts = [line.split('\n') for line in fh.read().split('\\')]

        letter_positions = [UNIT * 6, UNIT * 9, UNIT * 12, UNIT * 18]
        for i, part in enumerate(parts):
            image = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)

            @enumerate_function(part)
            def store(x, y, char):
                if char in CHAR_TO_BLOCK:
                    pos = get_pos_from_relative(pg.Vector2(x, y))
                    block = CHAR_TO_BLOCK[char](pos)
                    image.blit(block.image, pos)

            LogoBlock(pg.Vector2(letter_positions[i], UNIT * 6), image, i).add(self.group)

    def draw(self, canvas_screen):
        self.group.update(mouse_pos=pg.mouse.get_pos())
        self.group.draw(canvas_screen)


class Game:
    def __init__(self):
        self.logger = get_logger()
        self.data_handler = SaveHandler(self.logger)
        update_colours(self.data_handler)

        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.canvas_screen = pg.surface.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen = pg.display.get_surface()

        self.current_level = ''

        self.logo: Logo = Logo()
        self.cover: Cover = Cover()
        self.wave: Wave = Wave()

        self.bg_group: pg.sprite.Group = pg.sprite.Group()
        self.static_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)
        self.level_group: pg.sprite.Group = pg.sprite.Group()

        self.game_status = GameStatus.INITIALISING
        if not self.data_handler.get_option('has_adjusted_brightness'):
            self.load_adjust_brightness()
        else:
            self.load_splash_screen()

    def events(self):
        for event in pg.event.get():
            # keydown input
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()

            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.logger.info('exiting program gracefully')
                self.running = False

    def render(self):
        self.final_screen.fill(BG_COL)
        self.canvas_screen.fill(BG_COL)

        # RENDER HERE
        if not self.game_status == GameStatus.ADJUST_BRIGHTNESS:
            self.bg_group.draw(self.canvas_screen)
            self.canvas_screen.blit(self.static_surface, pg.Vector2(0, 0))
            self.level_group.draw(self.canvas_screen)

            # if self.on_splash_screen:
            #     self.cover.pos = pg.Vector2(0, pg.mouse.get_pos()[1])
            self.cover.draw(self.canvas_screen)
            self.wave.draw(self.canvas_screen, self.cover)
            self.logo.draw(self.canvas_screen)

        # FINAL RENDERING
        scaled = pg.transform.scale(self.canvas_screen, pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen.blit(scaled, pg.Vector2(0, 0))

        pg.display.flip()

    def load_level(self, level_name, side_load=False):
        level = parse_level_file(level_name)
        if not side_load:
            self.clear_current_level()
            self.current_level = level_name

        @enumerate_function(level)
        def store(x, y, char):
            if char in OUTLINE_CHARS:
                self.cover.add_outline_sprite(OutlineBlock(get_pos_from_relative(pg.Vector2(x, y))))

            if char in CHAR_TO_BLOCK:
                sprite = CHAR_TO_BLOCK[char](get_pos_from_relative(pg.Vector2(x, y)))
                self.static_surface.blit(sprite.image, sprite.rect)

    def load_adjust_brightness(self):
        self.game_status = GameStatus.ADJUST_BRIGHTNESS

    def load_splash_screen(self):
        self.game_status = GameStatus.SPLASH_SCREEN
        self.logo.create_logo()
        self.load_level('lobby', side_load=True)

    def clear_current_level(self):
        self.current_level = ''
        self.bg_group.empty()
        self.cover.empty()
        self.static_surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)
        self.level_group.empty()

    def main_loop(self):
        while self.running:
            self.events()
            self.render()

            self.clock.tick(self.fps)

            pg.display.set_caption("{} - fps: {:.2f}".format("1.ab REMASTER", self.clock.get_fps()))


def get_pos_from_relative(rel_pos: pg.Vector2) -> pg.Vector2:
    return pg.Vector2((rel_pos.x * UNIT) + MARGIN, (rel_pos.y * UNIT) + MARGIN)


def get_relative_from_pos(pos: pg.Vector2) -> pg.Vector2:
    return pg.Vector2((pos.x - MARGIN) / UNIT, (pos.y - MARGIN) / UNIT)


if __name__ == "__main__":
    pg.init()
    pg.display.set_icon(pg.image.load('baller.png'))
    pg.display.set_mode(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))

    game = Game()
    game.main_loop()

    pg.quit()
