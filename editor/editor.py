from constants import *
from utility import *
from lab_main import CHAR_TO_BLOCK
from button import BTNOperation, Button, ButtonOutlined


class Level:
    def __init__(self, level_file: str, pos: pg.Vector2):
        self.pos = pos
        self.level_file = level_file
        self.static_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)

    def init_level(self):
        level = parse_level_file(self.level_file)

        @enumerate_function(level)
        def store(x, y, char):
            if char in CHAR_TO_BLOCK:
                sprite = CHAR_TO_BLOCK[char](get_pos_from_relative(pg.Vector2(x, y)))
                self.static_surface.blit(sprite.image, sprite.rect)

    def draw(self, canvas_screen: pg.surface.Surface):
        canvas_screen.blit(self.static_surface, self.pos)

    def update(self):
        pass


class Editor:
    def __init__(self, logger):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.logger = logger

        self.canvas_screen = pg.surface.Surface(pg.Vector2(EDITOR_SCRN_WIDTH, EDITOR_SCRN_HEIGHT))
        self.final_screen = pg.display.get_surface()

    def events(self):
        for event in pg.event.get():
            # key input
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()

            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.logger.info('exiting program gracefully')
                self.running = False

    def render(self):
        self.final_screen.fill(Colours.BG_COL)
        self.canvas_screen.fill(Colours.BG_COL)

        # RENDER HERE

        # FINAL RENDERING
        scaled = pg.transform.scale(self.canvas_screen, pg.Vector2(EDITOR_SCRN_WIDTH, EDITOR_SCRN_HEIGHT))
        self.final_screen.blit(scaled, pg.Vector2(0, 0))

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.render()

            self.clock.tick(self.fps)

            pg.display.set_caption("1.ab REMASTER: EDITOR - fps: {:.2f}".format(self.clock.get_fps()))


def run_editor(logger: logging.Logger):
    logger.info('opening editor app')

    pg.init()
    pg.display.set_icon(pg.image.load('baller.png'))
    pg.display.set_mode(pg.Vector2(EDITOR_SCRN_WIDTH, EDITOR_SCRN_HEIGHT))

    editor = Editor(logger)
    editor.main_loop()

    pg.quit()
