import os.path
from pprint import pprint

import pygame as pg

block = pg.Surface(pg.Vector2(10, 10))
block.fill((255, 255, 255))

UNIT = 20
CHAR_TO_BLOCK = {
    '#': block
}


def parse_level_file(level_name):
    file_name = 'levels/' + level_name.split('.')[0] + '.txt'
    if not os.path.exists(file_name):
        raise FileNotFoundError(f'Cannot find file {file_name}')

    with open(file_name) as fh:
        return fh.read().split('\n')


class Block:
    def __init__(self, pos, colour=pg.Color(255, 255, 255), size=pg.Vector2(UNIT, UNIT)):
        self.pos: pg.Vector2 = pos
        self.colour: pg.Color = colour
        self.size: pg.Vector2 = size

    def draw(self, screen):
        pg.draw.rect(screen, self.colour, pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.canvas_screen = pg.surface.Surface(pg.Vector2(400, 600))
        self.final_screen = pg.display.get_surface()

        self.current_level = 'lobby'
        self.level_blocks = []

        lobby = parse_level_file(self.current_level)
        for y, row in enumerate(lobby):
            for x, char in enumerate(row):
                if char in CHAR_TO_BLOCK:
                    self.level_blocks.append(Block(pg.Vector2(x, y), size=pg.Vector2(1, 1)))

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
        for b in self.level_blocks:
            b.draw(self.canvas_screen)

        # FINAL RENDERING
        scaled = pg.transform.scale(self.canvas_screen, pg.Vector2(400, 600))
        self.final_screen.blit(scaled, pg.Vector2(0, 0))

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.events()
            self.render()

            self.clock.tick(self.fps)

            pg.display.set_caption("{} - fps: {:.2f}".format("1.ab REMASTER", self.clock.get_fps()))


if __name__ == "__main__":
    pg.init()
    pg.display.set_mode(pg.Vector2(400, 600))

    game = Game()
    game.main_loop()

    pg.quit()
