from pyglet.sprite import Sprite
import toyblock
from .system import graphics, physics, platform
from .components import Body, Platform, PlatformSprite, FloorCollision, Collision

def create(assets):
    global car
    global platform
    car = toyblock.Pool(
        1,
        (Body, FloorCollision, Sprite),
        ((True,), (*(0.0, 0.0), *(8.0, 0.0)), (assets["car"],)),
        systems=(physics, graphics))

    platform = toyblock.Pool(
        8,
        (Body, Platform, PlatformSprite),
        (None, None, (assets["block"],)),
        systems=(physics, platform)
    )

    @platform.init
    def init_platform(entity):
        entity[Platform].size = 4
