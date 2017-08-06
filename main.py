#!/usr/bin/env python

from random import choice, randrange
import pyglet
from pyglet.sprite import Sprite
import game.pool as pool
import game.system as system
from game.components import Body, PlatformSprite, Collision, FloorCollision, Input

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

class GameState:
    PLATFORM_PER_SEC = 2.
    SPEED = 8
    GRAVITY = system.GameWindow.VWIDTH

    @property
    def platforms(self):
        return self._platforms

    @property
    def car(self):
        return self._car

    def __init__(self, window):
        self._window = window
        self._platforms = []
        self._platform_time = 0.0
        self._distance = 0.
        self._car = None
        self.max_fuel = 100.0
        self.fuel = 100.0
        self._speed = 8

    def loop(self, dt):
        self._platform_time += dt
        self._distance += self._speed*dt
        if self._distance > Body.JUMP/4.:
            self._generate_random_platform(system.GameWindow.VHEIGHT + 8., -GameState.SPEED)
            self._distance = 0.
        if self._car is not None and self.fuel > 0.0:
            if self._car[Body].vel_x > 0.0:
                self.fuel += -dt*2.
            else:
                self.fuel += -dt*1.
        self._window.set_fuel(self.fuel, self.max_fuel)

    def _generate_random_platform(self, y, vel_y=0.):
        size = choice((3, 7))
        x = randrange(system.GameWindow.VWIDTH - size*8.0)
        self.create_platform(x, y, size, vel_y)

    def init(self):
        game_state.create_platform(0., 0., system.GameWindow.VWIDTH//8, -GameState.SPEED)
        y = 8.0
        while y < system.GameWindow.VHEIGHT:
            print(y)
            y += system.GameWindow.VHEIGHT/4.
            self._generate_random_platform(y, -GameState.SPEED)

        self.create_car(64.0, 8.)

    def create_platform(self, x, y, size, vel_y=0.):
        a_platform = pool.platform.get()
        self._window.add_Sprite(a_platform[PlatformSprite])
        a_platform[Body].x = x
        a_platform[Body].y = y
        a_platform[Body].vel_y = vel_y
        self._platforms.append(a_platform)
        collision = a_platform[Collision]
        collision.width = size*8.0
        collision.height = 8.0
        a_platform[PlatformSprite].size = size

    def create_car(self, x, y):
        car = pool.car.get()
        self._window.add_Sprite(car[Sprite])
        car[Body].x = x
        car[Body].y = y
        self._window.push_handlers(car[Input])
        self._car = car

    def free(self, entity):
        if entity.pool == pool.platform:
            self._window.remove_Sprite(entity[PlatformSprite])
            self._platforms.remove(entity)
        else:
            self._window.remove_Sprite(entity[Sprite])

if __name__ == "__main__":
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = system.GameWindow(system.GameWindow.VWIDTH,
        system.GameWindow.VHEIGHT, caption="Fuel4TheLight")
    icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
            get_image_data())
    game_window.set_icon(icon)

    pool.create(assets)
    game_state = GameState(game_window)

    pool.platform.clean(game_state.free)
    pyglet.clock.schedule(game_state.loop)
    pyglet.clock.schedule(system.do, -GameState.GRAVITY, game_state.platforms)

    game_state.init()

    pyglet.app.run()
