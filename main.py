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

assets_images = {
    "car": "car.png",
    "block": "block.png",
    "darkness": "darkness.png",
    "fuel": "fuel.png",
}

assets_sounds = {
    "second_jump": "second_jump.wav",
    "event": "event.wav"
}

class Title(Scene):
    def __init__(self, assets):
        super().__init__(1)

        Label = pyglet.text.Label

        self._cursor = 0
        self._menu = [
            Label("Start", x=64., y=128., group=self.group[0], batch=self.batch),
            Label("Quit", x=64., y=64., group=self.group[0], batch=self.batch)
        ]
        self._action = [
            self._start,
            self._quit
        ]
        self._cursor_sprite = Sprite(assets["car"], x=32.,y=self._menu[0].y, group=self.group[0], batch=self.batch)

        title = pyglet.text.Label("Fuel4TheLight", group=self.group[0], batch=self.batch)
        self._sounds = {
            "select": pyglet.media.StaticSource(assets["event"])
        }

    def _quit(self):
        pyglet.app.exit()

    def _start(self):
        print("and...action!")

    def on_key_press(self, symbol, modifiers):
        if symbol == key.DOWN and self._cursor + 1 < len(self._menu):
            self._cursor += 1
            self._cursor_sprite.y = self._menu[self._cursor].y
            self._sounds["select"].play()
        elif symbol == key.UP and self._cursor - 1 >= 0:
            self._cursor -= 1
            self._cursor_sprite.y = self._menu[self._cursor].y
            self._sounds["select"].play()
        elif symbol == key.RETURN:
            self._sounds["select"].play()
            self._action[self._cursor]()

if __name__ == "__main__":
    from game.director import Director
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_images[key]) for key in assets_images}
    assets.update({key : pyglet.resource.media(assets_sounds[key], False) for key in assets_sounds})
    #icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
    #        get_image_data())
    #game_window.set_icon(icon)

    title = Title(assets)
    engine = Engine(assets)
    director = Director(
        game.constants.VWIDTH*2, game.constants.VHEIGHT*2,
        caption="Fuel4TheLight",
        vwidth=game.constants.VWIDTH, vheight=game.constants.VHEIGHT)
    director.scene = title

    pyglet.app.run()
