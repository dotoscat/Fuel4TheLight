from pyglet.window import key
from pyglet.sprite import Sprite

class Input(object):
    JUMP = key.UP
    LEFT = key.LEFT
    RIGHT = key.RIGHT

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def jump(self):
        return self._jump

    def __init__(self, max_jumps=2):
        self._left = False
        self._right = False
        self._jump = False
        self._MAX_JUMPS = max_jumps
        self._jumps = max_jumps
        self.jump_pressed = False

    def reset_jumps(self):
        self._jumps = self._MAX_JUMPS

    def on_key_press(self, symbol, modifiers):
        self._left = self._left or symbol == Input.LEFT
        self._right = self._right or symbol == Input.RIGHT
        self._jump = self._jump or symbol == Input.JUMP
        self.jump_pressed = True if symbol == Input.JUMP else self.jump_pressed

    def on_key_release(self, symbol, modifiers):
        self._left = False if self._left and symbol == Input.LEFT else self._left
        self._right = False if self._right and symbol == Input.RIGHT else self._right
        self._jump = False if self._jump and symbol == Input.JUMP else self._jump

class Body(object):
    SPEED = 64.0
    JUMP = 128.0
    def __init__(self, gravity=False):
        self.x = 0.0
        self.y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.gravity = gravity

    def update(self, dt, gravity):
        if self.gravity: self.vel_y += gravity*dt
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt

class FloorCollision(object):
    def __init__(self, x1, y1, x2, y2):
        self._xy1 = (x1, y1)
        self._xy2 = (x2, y2)
        self.platform = None
        self.touch_floor = False

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
