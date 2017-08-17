#!/usr/bin/env python

from enum import Enum
from random import choice, randrange
import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite
import game.system as system
from game.components import (Body, PlatformSprite, Collision,
    FloorCollision, Input)
from game.constants import Type
import game.constants
from game.scene import Scene
from game.engine import Engine
from game import constants

assets_list = {
    "car": "car.png",
    "block": "block.png",
    "darkness": "darkness.png",
    "fuel": "fuel.png"
}

class GameState(Scene):

    class State(Enum):
        READY = 0
        RUNNING = 1
        PAUSED = 2
        GAME_OVER = 3

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
        self._last_platform_surface = None
        self._powerup = None

    def loop(self, dt):
        if self.fuel <= 0:
            self._state = GAME_OVER
        self._platform_time += dt
        self._distance += self._speed*dt
        if self._distance > Body.JUMP/4.:
            self._generate_random_platform(system.GameWindow.VHEIGHT + 8, -GameState.SPEED)
            self._distance = 0.
        if self._car is not None and self.fuel > 0.0:
            if self._car[Body].vel_x > 0.0:
                self.fuel += -dt*2.
            else:
                self.fuel += -dt*1.
        if self._powerup is None:
            self.create_powerup(128, 128)
        self._window.set_fuel(self.fuel, self.max_fuel)

    def _generate_random_platform(self, y, vel_y=0.):
        size = choice((3, 7))
        width = size*8.0
        VWIDTH = system.GameWindow.VWIDTH
        if self._last_platform_surface is None:
            x = randrange(VWIDTH-width)
        else:
            lx = self._last_platform_surface[0]
            lwidth = self._last_platform_surface[1]
            if lx + lwidth <= VWIDTH/2.:
                x = randrange(lx + lwidth, lx + lwidth + (VWIDTH/2. - lwidth))
            else:
                x = randrange(lx-VWIDTH/2., lx)
                x = 0. if x < 0 else x
        self._last_platform_surface = (x, width)
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
        a_platform[PlatformSprite].visible = True
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
        car[Sprite].visible = True
        car[Body].x = x
        car[Body].y = y
        collision = car[Collision]
        collision.width = 8.
        collision.height = 8.
        collision.type = Type.PLAYER
        collision.collides_with = Type.POWERUP
        self._window.push_handlers(car[Input])
        self._car = car

    def create_powerup(self, x, y):
        fuel = pool.powerup.get()
        fuel[FloorCollision].reset()
        fuel[Sprite].visible = True
        fuel[Body].x = x
        fuel[Body].y = y
        fuel[Body].vel_y = 0.
        collision = fuel[Collision]
        collision.type = Type.POWERUP
        collision.width = 8.
        collision.height = 8.
        self._powerup = fuel

    def increase_fuel(self, fuel=10.):
        self.fuel += fuel
        if self.fuel > self.max_fuel:
            self.fuel = self.max_fuel

    def decrease_fuel(self, fuel):
        self.fuel -= fuel
        if self.fuel < 0.:
            self.fuel = 0.

    def free(self, entity):
        if entity.pool == pool.platform:
            entity[PlatformSprite].visible = False
            self._platforms.remove(entity)
        else:
            entity[Sprite].visible = False
        if entity == self._car: print("GAME OVER!")
        if entity == self._powerup: self._powerup = None

class Title(Scene):
    def __init__(self, assets):
        super().__init__(1)

        Label = pyglet.text.Label

        self._cursor = 0
        self._menu = [
            Label("Tomate", x=64., y=128., group=self.group[0], batch=self.batch),
            Label("Pimiento", x=64., y=64., group=self.group[0], batch=self.batch)
        ]
        self._cursor_sprite = Sprite(assets["car"], x=32.,y=self._menu[0].y, group=self.group[0], batch=self.batch)

        title = pyglet.text.Label("Hola mundo", group=self.group[0], batch=self.batch)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP and self._cursor + 1 < len(self._menu):
            self._cursor += 1
            self._cursor_sprite.y = self._menu[self._cursor].y
        elif symbol == key.DOWN and self._cursor - 1 >= 0:
            self._cursor -= 1
            self._cursor_sprite.y = self._menu[self._cursor].y
        elif symbol == key.RETURN:
            print(self._cursor)

if __name__ == "__main__":
    from game.director import Director
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    #game_window = system.GameWindow(assets, system.GameWindow.VWIDTH*2,
    #    system.GameWindow.VHEIGHT*2, caption="Fuel4TheLight")
    #icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
    #        get_image_data())
    #game_window.set_icon(icon)

    #pool.create(assets, game_window.batch, game_window.layer)
    #game_state = GameState(game_window)

    #pool.platform.clean(game_state.free)
    #pool.powerup.clean(game_state.free)
    #pool.car.clean(game_state.free)
    #pyglet.clock.schedule(game_state.loop)
    #pyglet.clock.schedule(system.do, -GameState.GRAVITY, game_state)

    #game_state.init()
    Title = Title(assets)
    engine = Engine(assets)
    director = Director(
        game.constants.VWIDTH*2, game.constants.VHEIGHT*2,
        caption="Fuel4TheLight",
        vwidth=game.constants.VWIDTH, vheight=game.constants.VHEIGHT)
    director.scene = engine

    pyglet.app.run()
