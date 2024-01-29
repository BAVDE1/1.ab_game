import math

from constants import *


class BaseBlock(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2):
        super().__init__()
        self._og_pos: pg.Vector2 = pos
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
        block.blit(inside, pg.Vector2(UNIT / 4, UNIT / 4))
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
            cover_pos: pg.Vector2 = kwargs['cover_pos']
            self.pos = self.og_pos - cover_pos

        if 'mouse_pos' in kwargs:
            mouse_pos: pg.Vector2 = kwargs['mouse_pos']
            radius = 4
            mid = UNIT / 2
            vec = pg.Vector2(mouse_pos.x - mid, mouse_pos.y - mid) - self.og_pos
            if vec.length() > 0:
                self.pos -= (vec.normalize() * radius)
        return None

    @property
    def colour(self) -> pg.Color:
        return COL_LIGHT_GREY

    @property
    def size(self) -> pg.Vector2:
        return pg.Vector2(25, 25) # unit*1.25

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos.x + ((UNIT - self.size.x) / 2), self.pos.y + ((UNIT - self.size.y) / 2), self.size.x, self.size.y)


class LogoBlock(BaseBlock):
    def __init__(self, pos: pg.Vector2, _image: pg.Surface, i: int):
        super().__init__(pos)
        self._image = _image
        self._i = i

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.pos.y = self.og_pos.y + (0.2 * math.sin(2 * (time.time() - (1 + (self._i * 0.5)))))
        # self.pos.y = self.og_pos.y + math.sin(self._i * time.time())
        return None

    @property
    def image(self) -> pg.Surface:
        return self._image

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos.x, self.pos.y, self.image.get_size()[0], self.image.get_size()[1])
