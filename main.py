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
