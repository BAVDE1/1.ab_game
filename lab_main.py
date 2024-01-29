from blocks import BaseBlock, FancyBlock, PlatformBlock, GreyBlock, LightGreyBlock, OutlineBlock, LogoBlock
from constants import *


CHAR_TO_BLOCK = {
    '#': BaseBlock,
    '*': FancyBlock,
    '-': PlatformBlock,

    ':': LightGreyBlock,
    '.': GreyBlock,
}
OUTLINE_CHARS = ['#', '*', '-']


def parse_level_file(level_name):
    file_name = 'files/' + level_name.split('.')[0] + '.txt'
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
        self.pos: pg.Vector2 = pg.Vector2(0, 0)
        self.cover_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.outline_group: pg.sprite.Group = pg.sprite.Group()

    def add_outline_sprite(self, sprite: pg.sprite.Sprite):
        sprite.add(self.outline_group)

    def empty(self):
        self.outline_group.empty()

    def update(self):
        self.outline_group.update(mouse_pos=pg.Vector2(pg.mouse.get_pos()), cover_pos=self.pos)

    def draw(self, canvas_screen: pg.Surface):
        self.update()

        self.cover_surface.fill(BG_COL)
        self.outline_group.draw(self.cover_surface)
        canvas_screen.blit(self.cover_surface, self.pos)


class Logo:
    def __init__(self):
        self.pos: pg.Vector2 = pg.Vector2()
        self.group: pg.sprite.Group = pg.sprite.Group()

    def create_logo(self):
        with open('files/logo.txt') as fh:
            parts = [line.split('\n') for line in fh.read().split('\\')]

        letter_positions = [[120, 120], [180, 120], [240, 120], [360, 120]]
        for i, part in enumerate(parts):
            image = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)

            @enumerate_function(part)
            def store(x, y, char):
                if char in CHAR_TO_BLOCK:
                    pos = get_pos_from_relative(pg.Vector2(x, y))
                    block = CHAR_TO_BLOCK[char](pos)
                    image.blit(block.image, pos)

            LogoBlock(pg.Vector2(letter_positions[i]), image, i).add(self.group)

    def draw(self, canvas_screen):
        self.group.update()
        self.group.draw(canvas_screen)


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.canvas_screen = pg.surface.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen = pg.display.get_surface()

        self.current_level = ''
        self.on_splash_screen = False

        self.logo: Logo = Logo()
        self.cover: Cover = Cover()

        self.bg_group: pg.sprite.Group = pg.sprite.Group()
        self.static_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)
        self.level_group: pg.sprite.Group = pg.sprite.Group()

        # self.load_level('lobby')
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

        if not self.on_splash_screen:
            self.cover.pos = pg.Vector2(0, pg.mouse.get_pos()[1])
        self.cover.draw(self.canvas_screen)
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

    def load_splash_screen(self):
        self.on_splash_screen = True
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
