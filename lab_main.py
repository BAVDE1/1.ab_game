from blocks import BaseBlock, FancyBlock, PlatformBlock, GreyBlock, LightGreyBlock, BgBlock
from constants import *


CHAR_TO_BLOCK = {
    '#': BaseBlock,
    '*': FancyBlock,
    '-': PlatformBlock,

    ':': LightGreyBlock,
    '.': GreyBlock,
}


def parse_level_file(level_name):
    file_name = 'files/' + level_name.split('.')[0] + '.txt'
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f'Cannot find file {file_name}')

    with open(file_name) as fh:
        return fh.read().split('\n')


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.canvas_screen = pg.surface.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen = pg.display.get_surface()

        self.current_level = ''
        self.bg_blocks: pg.sprite.Group = pg.sprite.Group()
        self.level_blocks: pg.sprite.Group = pg.sprite.Group()

        self.load_level('lobby')

    def events(self):
        for event in pg.event.get():
            # keydown input
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()

            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False

    def render(self):
        fill_col = (0, 5, 5)
        self.final_screen.fill(fill_col)
        self.canvas_screen.fill(fill_col)

        # RENDER HERE
        self.bg_blocks.update(mouse_pos=pg.mouse.get_pos())
        self.bg_blocks.draw(self.canvas_screen)
        self.level_blocks.draw(self.canvas_screen)

        # FINAL RENDERING
        scaled = pg.transform.scale(self.canvas_screen, pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen.blit(scaled, pg.Vector2(0, 0))

        pg.display.flip()

    def load_level(self, level_name):
        self.current_level = level_name
        level = parse_level_file(level_name)
        for y, row in enumerate(level):
            for x, char in enumerate(row):
                if char in CHAR_TO_BLOCK:
                    if char in ('#', '*', '-'):
                        BgBlock(get_pos_from_relative(pg.Vector2(x, y))).add(self.bg_blocks)
                    self.level_blocks.add(CHAR_TO_BLOCK[char](get_pos_from_relative(pg.Vector2(x, y))))

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
    pg.display.set_mode(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))

    game = Game()
    game.main_loop()

    pg.quit()
