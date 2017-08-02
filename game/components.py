from pyglet.window import key
from pyglet.sprite import Sprite

class Body(object):
    SPEED = 64.0
    JUMP = 128.0
    def __init__(self, gravity=False):
        self.x = 0.0
        self.y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.gravity = gravity
        self.jumped = False
        self.jumps = 1
        self.touch_floor = False

    def update(self, dt, gravity):
        if self.gravity: self.vel_y += gravity*dt
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.vel_x = -Body.SPEED
        if symbol == key.RIGHT:
            self.vel_x = Body.SPEED
        if self.touch_floor and not self.jumped and symbol == key.UP:
            self.vel_y = Body.JUMP
            self.jumped = True
            self.gravity = True
        elif not self.touch_floor and self.jumps > 0 and symbol == key.UP:
            self.vel_y = Body.JUMP/2.0
            self.jumps -= 1

    def on_key_release(self, symbol, modifiers):
        if ((symbol == key.LEFT and self.vel_x < 0.0) or
        (symbol == key.RIGHT and self.vel_x > 0.0)):
            self.vel_x = 0.0
        elif symbol == key.UP and self.jumped and self.jumps > 0:
            self.vel_y = 0.0

class FloorCollision(object):
    def __init__(self, x1, y1, x2, y2):
        self._xy1 = (x1, y1)
        self._xy2 = (x2, y2)
        self.platform = None

    def get_points(self, x, y):
        xy1 = self._xy1
        xy2 = self._xy2
        return ((x + xy1[0], y + xy1[1]), (x + xy2[0], y + xy2[1]))

class Collision(object):
    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y + self.height

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.width = 0.0
        self.height = 0.0

    def __contains__(self, pair):
        return self.x <= pair[0] <= self.right and self.y <= pair[1] <= self.top

class PlatformSprite(object):
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        sprites = self._sprites
        for i in range(self._size):
            sprites[i].x = x+i*8.

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        for sprite in self._sprites:
            sprite.y = y

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        texture = self._texture
        self._sprites = [Sprite(texture, self._x+i*8., self._y) for i in range(size)]
        self._size = size

    def __init__(self, texture):
        self._texture = texture
        self._x = 0.0
        self._y = 0.0
        self._size = 0

    def draw(self):
        x = self.x
        y = self.y
        sprites = self._sprites
        for sprite in sprites: sprite.draw()
