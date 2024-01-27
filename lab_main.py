from blocks import BaseBlock, FancyBlock, PlatformBlock, GreyBlock, LightGreyBlock, OutlineBlock
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


class Cover:
    def __init__(self):
        self.pos: pg.Vector2 = pg.Vector2(0, 0)
        self.cover_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.outline_group: pg.sprite.Group = pg.sprite.Group()

    def add_outline_sprite(self, sprite: pg.sprite.Sprite):
        sprite.add(self.outline_group)

    def empty(self):
        self.outline_group.empty()

    def update(self):
        self.pos = pg.Vector2(pg.mouse.get_pos()) / 2
        self.outline_group.update(mouse_pos=pg.Vector2(pg.mouse.get_pos()), cover_pos=self.pos)

    def draw(self, canvas_screen: pg.Surface):
        self.update()

        self.cover_surface.fill(BG_COL)
        self.outline_group.draw(self.cover_surface)
        canvas_screen.blit(self.cover_surface, self.pos)


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.canvas_screen = pg.surface.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen = pg.display.get_surface()

        self.current_level = ''

        self.cover: Cover = Cover()
        self.bg_group: pg.sprite.Group = pg.sprite.Group()
        self.static_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)
        self.level_group: pg.sprite.Group = pg.sprite.Group()

        self.load_splash_screen()

    def events(self):
        for event in pg.event.get():
            # keydown input
            if event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()

            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False

    def render(self):
        self.final_screen.fill(BG_COL)
        self.canvas_screen.fill(BG_COL)

        # RENDER HERE
        self.bg_group.draw(self.canvas_screen)
        self.canvas_screen.blit(self.static_surface, pg.Vector2(0, 0))
        self.level_group.draw(self.canvas_screen)

        self.cover.draw(self.canvas_screen)

        # FINAL RENDERING
        scaled = pg.transform.scale(self.canvas_screen, pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen.blit(scaled, pg.Vector2(0, 0))

        pg.display.flip()

    def load_level(self, level_name, side_load=False):
        level = parse_level_file(level_name)
        if not side_load:
            self.clear_current_level()
            self.current_level = level_name

        for y, row in enumerate(level):
            for x, char in enumerate(row):
                if char in CHAR_TO_BLOCK:
                    if char in ('#', '*', '-'):
                        self.cover.add_outline_sprite(OutlineBlock(get_pos_from_relative(pg.Vector2(x, y))))

                    sprite = CHAR_TO_BLOCK[char](get_pos_from_relative(pg.Vector2(x, y)))
                    self.static_surface.blit(sprite.image, sprite.rect)

    def load_splash_screen(self):
        self.load_level('logo')
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
    pg.display.set_mode(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))

    game = Game()
    game.main_loop()

    pg.quit()
