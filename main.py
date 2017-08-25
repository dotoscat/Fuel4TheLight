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
from game.gui import Menu, FractionLabel
from game.director import Director

TITLE = "Fuel4TheLight"
AUTHOR = "Oscar Triano @cat_dotoscat"
VERSION = "1.0.0"
LICENSE = "GPL-3.0"

assets_images = {
    "car_left": {"name": "car.png"},
    "car_right": {"name": "car.png", "flip_x": True},
    "block": {"name": "block.png"},
    "darkness": {"name": "darkness.png"},
    "fuel": {"name": "fuel.png"},
}

assets_sounds = {
    "second_jump": "second_jump.wav",
    "event": "event.wav",
    "landing": "landing.wav",
    "fuel_pickup": "fuel_pickup.wav"
}

class Title(Scene):
    def __init__(self, assets, score):
        super().__init__(1)

        Label = pyglet.text.Label

        def start(menu):
            Director.set_scene("engine")

        def quit(menu):
            pyglet.app.exit()

        cursor_sprite = Sprite(assets["car_left"], group=self.group[0], batch=self.batch)
        self._score = score
        self._menu = Menu(cursor_sprite, 92., 64.)
        self._menu.add_entry(
            Label("Start", group=self.group[0], batch=self.batch),
            start, 16., 16.
        )
        self._menu.add_entry(
            Label("Quit", group=self.group[0], batch=self.batch),
            quit, 16., 0.
        )
        title = pyglet.text.Label(
            TITLE, group=self.group[0], batch=self.batch,
            anchor_x="center", anchor_y="center",
            x=constants.VWIDTH/2., y=constants.VHEIGHT - 16.,
            color=(255, 255, 0, 255)
        )
        author = Label(
            AUTHOR, group=self.group[0], batch=self.batch,
            anchor_x="center", anchor_y="center",
            x=title.x, y=title.y-16.,
            font_size=8
        )
        self._score_label = FractionLabel(
            4, '0', group=self.group[0], batch=self.batch,
            y=32.
        )
        version = Label(
            'ver.' + VERSION, group=self.group[0], batch=self.batch,
            x=0., y=0.,
            font_size=8
        )
        self._sounds = {
            "select": pyglet.media.StaticSource(assets["event"])
        }

    def init(self):
        self._score_label.set(self._score.meters, self._score.top)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP and self._menu.move_up():
            self._sounds["select"].play()
        elif symbol == key.DOWN and self._menu.move_down():
            self._sounds["select"].play()
        elif symbol == key.RETURN:
            self._menu.execute()
            self._sounds["select"].play()

if __name__ == "__main__":
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(**assets_images[key]) for key in assets_images}
    assets.update({key : pyglet.resource.media(assets_sounds[key], False) for key in assets_sounds})
    assets["car_right"].anchor_x = 0.
    #icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
    #        get_image_data())
    #game_window.set_icon(icon)

    class Score:
        def __init__(self):
            self.meters = 0
            self.top = 0

        def __iadd__(self, value):
            self.meters += value
            if self.meters > self.top:
                self.top = self.meters

    score = Score()

    title = Title(assets, score)
    engine = Engine(assets)
    director = Director(
        game.constants.VWIDTH*2, game.constants.VHEIGHT*2,
        caption="Fuel4TheLight",
        vwidth=game.constants.VWIDTH, vheight=game.constants.VHEIGHT)
    Director.add_scene("title", title)
    Director.add_scene("engine", engine)
    Director.set_scene("title")

    pyglet.app.run()
