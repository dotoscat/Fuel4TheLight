from pyglet.window import key

class Body(object):
    SPEED = 32.0

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

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.vel_x = -Body.SPEED
        if symbol == key.RIGHT:
            self.vel_x = Body.SPEED

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.LEFT, key.RIGHT):
            self.vel_x = 0.0

class FloorCollision(object):
    def __init__(self, x1, y1, x2, y2):
        self._xy1 = (x1, y1)
        self._xy2 = (x2, y2)

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
        return self.x < pair[0] < self.right and self.y < pair[1] < self.top

class Platform(object):
    def __init__(self):
        self.size = 0

class PlatformSprite(object):
    def __init__(self, texture):
        self.texture = texture
        self.x = 0.0
        self.y = 0.0
        self.times = 0
    def draw(self):
        x = self.x
        y = self.y
        times = self.times
        for i in range(times): self.texture.blit(x + i*8.0, y)
