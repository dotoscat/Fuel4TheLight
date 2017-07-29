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
