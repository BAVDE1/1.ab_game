import pygame as pg


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()

        self.canvas_screen = pg.surface.Surface(pg.Vector2(400, 600))
        self.final_screen = pg.display.get_surface()

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
