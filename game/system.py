import pyglet
from pyglet.sprite import Sprite
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl
import toyblock
from .components import Body, Platform, PlatformSprite

class GameWindow(pyglet.window.Window):
    VWIDTH = 210
    VHEIGHT = 160
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprites = []

    def on_draw(self):
        self.clear()
        for sprite in self.sprites:
            sprite.draw()

    def add_Sprite(self, Sprite_):
        self.sprites.append(Sprite_)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, GameWindow.VWIDTH, 0, GameWindow.VHEIGHT, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)

@toyblock.system
def physics(system, entity, dt, gravity):
    body = entity[Body]
    body.update(dt, gravity)

@toyblock.system
def graphics(system, entity):
    body = entity[Body]
    entity[Sprite].set_position(body.x, body.y)

@toyblock.system
def platform(system, entity):
    body = entity[Body]
    platform = entity[PlatformSprite]
    platform.x = body.x
    platform.y = body.y
    platform.times = entity[Platform].size

def do(dt, gravity):
    physics(dt, gravity)
    graphics()
    platform()
