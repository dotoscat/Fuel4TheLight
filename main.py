#!/usr/bin/env python

import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl
import toyblock

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

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

if __name__ == "__main__":
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

    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = GameWindow(caption="Fuel4TheLight")
    icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
            get_image_data())
    game_window.set_icon(icon)

    car_pool = toyblock.Pool(
        1,
        (Body, Sprite),
        ((True,), (assets["car"],)),
        systems=(physics, graphics))

    platform_pool = toyblock.Pool(
        8,
        (Body, Platform, PlatformSprite),
        (None, None, (assets["block"],)),
        systems=(physics, platform)
    )
    @platform_pool.init
    def init_platform(entity):
        entity[Platform].size = 4

    def do_systems(dt):
        physics(dt, -32.0)
        graphics()
        platform()

    pyglet.clock.schedule(do_systems)

    car = car_pool.get()
    game_window.add_Sprite(car[Sprite])
    car[Body].x = 64.0
    car[Body].y = 64.0
    game_window.push_handlers(car[Body])

    a_platform = platform_pool.get()
    game_window.add_Sprite(a_platform[PlatformSprite])
    a_platform[Body].x = 32
    a_platform[Body].y = 32

    pyglet.app.run()
