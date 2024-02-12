import random
from utility import *
from blocks import BaseBlock, FancyBlock, PlatformBlock, GreyBlock, LightGreyBlock, OutlineBlock, LogoBlock, WaveBlock
from editor import editor


OUTLINE_CHARS = ['#', '*', '-']
CHAR_TO_BLOCK = {
    '#': BaseBlock,
    '*': FancyBlock,
    '-': PlatformBlock,

    ':': LightGreyBlock,
    '.': GreyBlock,
}


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

        self.cover_surface.fill(Colours.BG_COL)
        self.outline_group.draw(self.cover_surface)
        # for pos in self.bulge_positions:
        #     pg.draw.rect(self.cover_surface, (255, 0, 0), pg.Rect(pos.x - self.pos.x, pos.y - self.pos.y, 5, 5))

        canvas_screen.blit(self.cover_surface, self.pos)


class Wave:
    def __init__(self):
        self.pos: pg.Vector2 = pg.Vector2()
        self.wave_group: pg.sprite.Group = pg.sprite.Group(*[WaveBlock(pg.Vector2(x * UNIT, 0), x) for x in range(WIDTH)])  # generates necessary sprites

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


class AdjustBrightness:
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler

        self.up_keys = [pg.K_RIGHT, pg.K_d, pg.K_UP, pg.K_w]
        self.down_keys = [pg.K_LEFT, pg.K_a, pg.K_DOWN, pg.K_s]

        self.brightness_val = self.data_handler.get_option('brightness')
        self.max_val = self.data_handler.get_const('max_brightness')
        self.min_val = self.data_handler.get_const('min_brightness')

    def event(self, event):
        val = self.brightness_val
        if event.key in self.up_keys:
            val += 1
        elif event.key in self.down_keys:
            val -= 1
        if val != self.brightness_val:
            self.data_handler.set_option('brightness', val)
            self.brightness_val = self.data_handler.get_option('brightness')
            update_colours(self.data_handler)

    def draw(self, canvas_screen):
        pass


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.logger = get_logger()
        self.data_handler = DataHandler(self.logger)
        update_colours(self.data_handler)

        self.canvas_screen = pg.surface.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))
        self.final_screen = pg.display.get_surface()

        self.bg_group: pg.sprite.Group = pg.sprite.Group()
        self.static_surface: pg.Surface = pg.Surface(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT), pg.SRCALPHA)
        self.level_group: pg.sprite.Group = pg.sprite.Group()

        self.logo: Logo = Logo()
        self.cover: Cover = Cover()
        self.wave: Wave = Wave()
        self.adjust_brightness: AdjustBrightness = AdjustBrightness(self.data_handler)

        self.current_level = ''
        self.game_status = GameStatus.INITIALISING
        if not self.data_handler.get_option('has_adjusted_brightness'):
            self.load_adjust_brightness()
        else:
            self.load_splash_screen()

    def events(self):
        for event in pg.event.get():
            # key input
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()

                if self.game_status == GameStatus.ADJUST_BRIGHTNESS:
                    self.adjust_brightness.event(event)

                # close and run editor
                if self.game_status == GameStatus.SPLASH_SCREEN and event.key == pg.K_e:
                    self.logger.info('closing main app')
                    self.running = False
                    editor.run_editor(self.logger)

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
        if self.game_status == GameStatus.ADJUST_BRIGHTNESS:
            self.adjust_brightness.draw(self.canvas_screen)
        else:
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
        self.load_level('lobby')

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

            pg.display.set_caption("1.ab REMASTER - fps: {:.2f}".format(self.clock.get_fps()))


if __name__ == "__main__":
    pg.init()
    pg.display.set_icon(pg.image.load('baller.png'))
    pg.display.set_mode(pg.Vector2(SCRN_WIDTH, SCRN_HEIGHT))

    game = Game()
    game.main_loop()

    pg.quit()
