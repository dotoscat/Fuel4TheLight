from pyglet.window import key
from pyglet.sprite import Sprite
import toyblock
from .system import (update_graphics, physics, recycle,
    update_collision, platform_collision, update_platform_sprite, input_sys,
    do_collision)
from .components import (Body, PlatformSprite, FloorCollision, Collision, Input)
from .scene import Scene
from . import constants
from .hud import Bar

class Engine(Scene):
    def __init__(self, assets):
        super().__init__(3)
        self._pool = {
            "car": toyblock.Pool(
                1,
                (Input, Body, FloorCollision, Collision, Sprite),
                (None, (True,), (*(0.0, 0.0), *(8.0, 0.0)), None, (assets["car"],)),
                (None, None, None, None, {"subpixel": False, "group": self.group[1], "batch": self.batch}),
                systems=(input_sys, recycle, physics, update_graphics, update_collision, do_collision, platform_collision)
            ),
            "platform": toyblock.Pool(
                32,
                (Body, Collision, PlatformSprite),
                (None, None, (assets["block"],)),
                (None, None, {"group": self.group[0], "batch": self.batch}),
                systems=(physics, recycle, update_collision, update_platform_sprite)
            ),
            "powerup": toyblock.Pool(
                2,
                (Body, FloorCollision, Collision, Sprite),
                ((False,), (*(0., 0.), *(8., 0.)), None, (assets["fuel"], -32., -32.)),
                (None, None, None, {"subpixel": False, "group": self.group[1], "batch": self.batch}),
                systems=(physics, recycle, update_graphics, update_collision, do_collision, platform_collision)
            )
        }
        self._fuel = 100.
        self._MAX_FUEL = 100.
        self._fuel_bar = Bar(8, constants.VHEIGHT - 16, 64, 8, (0, 128, 255, 255), (0, 255, 128, 255))
        self._darkness = [
            Sprite(assets["darkness"], i*8., -4., batch=self.batch, group=self.group[2])
            for i in range(constants.VWIDTH//8)
        ]

    def on_key_press(self, key, mod):
        print(key, mod)

    def update(self, dt):
        self._fuel_bar.set_value(self._fuel, self._MAX_FUEL)

    def draw(self):
        super().draw()
        self._fuel_bar.draw()
