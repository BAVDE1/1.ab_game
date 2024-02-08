import math
import time

from constants import *


class BaseBlock(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2):
        super().__init__()
        self._og_pos: pg.Vector2 = pg.Vector2(pos)
        self.pos: pg.Vector2 = pos

    def update(self, *args: Any, **kwargs: Any) -> None:
        return None

    @property
    def og_pos(self):
        return self._og_pos

    @property
    def colour(self) -> pg.Color:
        return pg.Color(255, 255, 255)

    @property
    def size(self) -> pg.Vector2:
        return pg.Vector2(UNIT, UNIT)

    @property
    def image(self) -> pg.Surface:
        block = pg.Surface(self.size)
        block.fill(self.colour)
        return block

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def clone(self):
        return copy.deepcopy(self)


class FancyBlock(BaseBlock):
    @property
    def image(self) -> pg.Surface:
        block = pg.Surface(self.size)
        block.fill(self.colour)
        inside = pg.Surface(self.size * 0.5)
        inside.fill(pg.Color(0, 5, 5))
        block.blit(inside, pg.Vector2(UNIT * 0.25, UNIT * 0.25))
        return block


class PlatformBlock(BaseBlock):
    @property
    def size(self) -> pg.Vector2:
        return pg.Vector2(UNIT, UNIT / 2)


class GreyBlock(BaseBlock):
    @property
    def colour(self) -> pg.Color:
        return COL_GREY


class LightGreyBlock(BaseBlock):
    @property
    def colour(self) -> pg.Color:
        return COL_LIGHT_GREY


class OutlineBlock(BaseBlock):
    def update(self, *args: Any, **kwargs: Any) -> None:
        if 'cover_pos' in kwargs:
            cover_pos = pg.Vector2(kwargs['cover_pos'])
            self.pos = self.og_pos - cover_pos

        if 'bulge_positions' in kwargs:
            bulge_positions = list(kwargs['bulge_positions'])
            radius = UNIT * 0.14
            half_unit = UNIT * 0.5
            for bulge_pos in bulge_positions:
                bulge_pos = pg.Vector2(bulge_pos)
                vec = pg.Vector2(bulge_pos.x - half_unit, bulge_pos.y - half_unit) - self.og_pos
                if vec.length() > 0:
                    self.pos -= (vec.normalize() * radius)
        return None

    @property
    def colour(self) -> pg.Color:
        return COL_LIGHT_GREY

    @property
    def size(self) -> pg.Vector2:
        return pg.Vector2(UNIT * 1.3, UNIT * 1.3)

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos.x + ((UNIT - self.size.x) / 2), self.pos.y + ((UNIT - self.size.y) / 2), self.size.x, self.size.y)


class WaveBlock(OutlineBlock):
    def __init__(self, pos: pg.Vector2, x_index):
        super().__init__(pos)
        self._x = x_index
        self.spawn_time = time.time() + x_index

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.og_pos.y = kwargs['y_pos'] - (UNIT / 2)
        amp = UNIT * 0.2
        sine_time = time.time() - self.spawn_time
        self.pos.y = self.og_pos.y + (amp * math.sin(sine_time))
        return None

    @property
    def colour(self) -> pg.Color:
        return pg.Color(255, 255, 255)

    def __repr__(self):
        return f'WaveBlock({self.pos}, {self._x}, {len(self.groups())} group/s)'


class LogoBlock(BaseBlock):
    def __init__(self, pos: pg.Vector2, image: pg.Surface, i: int = 0):
        super().__init__(pos)
        self.spawn_time = time.time() + i
        self._image = image

    def update(self, *args: Any, **kwargs: Any) -> None:
        amp = UNIT * 0.4
        sine_time = time.time() - self.spawn_time
        self.pos.y = self.og_pos.y + (amp * math.sin(sine_time))
        return None

    @property
    def image(self) -> pg.Surface:
        return self._image

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos.x, self.pos.y, self.image.get_size()[0], self.image.get_size()[1])
