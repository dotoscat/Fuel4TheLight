import pyglet
from pyglet.sprite import Sprite
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl
import toyblock
from .components import Body, Platform, PlatformSprite, FloorCollision, Collision

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
def update_graphics(system, entity):
    body = entity[Body]
    entity[Sprite].set_position(body.x, body.y)

@toyblock.system
def update_platform(system, entity):
    body = entity[Body]
    platform = entity[PlatformSprite]
    platform.x = body.x
    platform.y = body.y
    platform.times = entity[Platform].size

@toyblock.system
def collision(system, entity):
    body = entity[Body]
    collision = entity[Collision]
    collision.x = body.x
    collision.y = body.y

@toyblock.system
def platform_collision(system, entity, platforms):
    body = entity[Body]
    x = body.x
    y = body.y
    floor_collision = entity[FloorCollision]
    for platform in platforms:
        platform_collision = platform[Collision]
        points = floor_collision.get_points(x, y)
        if points[0] not in platform_collision and points[1] not in platform_collision: continue
        body.y = platform_collision.top
        body.vel_y = 0.0
        break

def do(dt, gravity, platforms):
    physics(dt, gravity)
    update_platform()
    collision()
    platform_collision(platforms)
    update_graphics()
