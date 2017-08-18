from random import choice, randrange
from pyglet.window import key
from pyglet.sprite import Sprite
import toyblock
from .system import (update_graphics, physics, recycle,
    update_collision, platform_collision, update_platform_sprite, input_sys,
    do_collision)
from .system import do as do_systems
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
        self._platforms = []
        self._last_platform_surface = None
        self._distance = 0.
        self._speed = 8.

    @property
    def platforms(self):
        return self._platforms

    def _set_entity_component(entity, type, kwargs):
        component = entity[type]
        for key in kwargs:
            setattr(component, key, kwargs[key])

    def create_platform(self, x, y, size, vel_y=0.):
        a_platform = self._pool["platform"].get()
        Engine._set_entity_component(a_platform, Body, {"x": x, "y": y, "vel_y": vel_y})
        a_platform[PlatformSprite].visible = True
        self._platforms.append(a_platform)
        collision = a_platform[Collision]
        collision.width = size*8.0
        collision.height = 8.0
        a_platform[PlatformSprite].size = size

    def on_key_press(self, key, mod):
        print(key, mod)

    def update(self, dt):
        self._distance += self._speed*dt
        if self._distance > constants.JUMP/4.:
            self._generate_random_platform(constants.VHEIGHT + 8, -constants.SPEED)
            self._distance = 0.
        do_systems(dt, self)

    def _generate_random_platform(self, y, vel_y=0.):
        size = choice((3, 7))
        width = size*8.0
        VWIDTH = constants.VWIDTH
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

    def draw(self):
        super().draw()
        self._fuel_bar.set_value(self._fuel, self._MAX_FUEL)
        self._fuel_bar.draw()
