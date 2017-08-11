from pyglet.sprite import Sprite
import toyblock
from .system import (update_graphics, physics, update_platform,
    update_collision, platform_collision, update_platform_sprite, input_sys,
    do_collision)
from .components import (Body, PlatformSprite, FloorCollision, Collision, Input, Effect)

def create(assets, batch, layers):
    global car
    global platform
    global powerup
    car = toyblock.Pool(
        1,
        (Input, Body, FloorCollision, Collision, Sprite),
        (None, (True,), (*(0.0, 0.0), *(8.0, 0.0)), None, (assets["car"],)),
        # (None, None, None, {"subpixel": False}),
        (None, None, None, None, {"subpixel": False, "group": layers[1], "batch": batch}),
        systems=(input_sys, physics, update_graphics, update_collision, do_collision, platform_collision))

    platform = toyblock.Pool(
        32,
        (Body, Collision, PlatformSprite),
        (None, None, (assets["block"],)),
        (None, None, {"group": layers[0], "batch": batch}),
        systems=(physics, update_platform, update_collision, update_platform_sprite)
    )
    powerup = toyblock.Pool(
        2,
        (Effect, Body, FloorCollision, Collision, Sprite),
        (None, (False,), (*(0., 0.), *(8., 0.)), None, (assets["fuel"], -32., -32.)),
        (None, None, None, None, {"subpixel": False, "group": layers[1], "batch": batch}),
        systems=(physics, update_graphics, update_collision, do_collision, platform_collision)
    )
