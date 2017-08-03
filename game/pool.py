from pyglet.sprite import Sprite
import toyblock
from .system import update_graphics, physics, update_platform,\
    update_collision, platform_collision, update_platform_sprite, input_sys
from .components import Body, PlatformSprite, FloorCollision, Collision, Input

def create(assets):
    global car
    global platform
    car = toyblock.Pool(
        1,
        (Input, Body, FloorCollision, Sprite),
        (None, (False,), (*(0.0, 0.0), *(8.0, 0.0)), (assets["car"],)),
        (None, None, None, {"subpixel": False}),
        systems=(input_sys, physics, update_graphics, platform_collision))

    platform = toyblock.Pool(
        32,
        (Body, Collision, PlatformSprite),
        (None, None, (assets["block"],)),
        systems=(physics, update_platform, update_collision, update_platform_sprite)
    )
