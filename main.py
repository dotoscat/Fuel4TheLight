#!/usr/bin/env python

from random import choice, randrange
import pyglet
from pyglet.sprite import Sprite
import game.pool as pool
import game.system as system
from game.components import Body, Platform, PlatformSprite, Collision, FloorCollision

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

class GameState:
    PLATFORM_PER_SEC = 2.

    @property
    def platforms(self):
        return self._platforms

    def __init__(self, window):
        self._window = window
        self._platforms = []
        self._platform_time = 0.0

    def loop(self, dt):
        self._platform_time += dt
        if self._platform_time >= GameState.PLATFORM_PER_SEC and choice((True, False)):
            size = choice((3, 7))
            x = randrange(system.GameWindow.VWIDTH - size*8.0)
            self.create_platform(x, system.GameWindow.VHEIGHT + 8., size)
            self._platform_time = 0.

    def create_platform(self, x, y, size):
        a_platform = pool.platform.get()
        self._window.add_Sprite(a_platform[PlatformSprite])
        a_platform[Body].x = x
        a_platform[Body].y = y
        a_platform[Body].vel_y = -8.0
        self._platforms.append(a_platform)
        a_platform[Platform].size = size
        collision = a_platform[Collision]
        collision.width = size*8.0
        collision.height = 8.0

    def free(self, entity):
        if entity.pool == pool.platform:
            self._window.remove_Sprite(entity[PlatformSprite])
        else:
            self._window.remove_Sprite(entity[Sprite])

if __name__ == "__main__":
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = system.GameWindow(caption="Fuel4TheLight")
    icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
            get_image_data())
    game_window.set_icon(icon)

    pool.create(assets)

    game_state = GameState(game_window)

    pyglet.clock.schedule(system.do, -160.0, game_state.platforms)
    pyglet.clock.schedule_interval(game_state.loop, 1.)

    car = pool.car.get()
    pool.platform.clean(game_state.free)

    game_window.add_Sprite(car[Sprite])
    car[Body].x = 64.0
    car[Body].y = 64.0
    game_window.push_handlers(car[Body])

    game_state.create_platform(0., 0., system.GameWindow.VWIDTH//8)

    pyglet.app.run()
