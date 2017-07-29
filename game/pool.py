from pyglet.sprite import Sprite
import toyblock
from .system import update_graphics, physics, update_platform,\
    collision, platform_collision
from .components import Body, Platform, PlatformSprite, FloorCollision, Collision

def create(assets):
    global car
    global platform
    car = toyblock.Pool(
        1,
        (Body, FloorCollision, Sprite),
        ((True,), (*(0.0, 0.0), *(8.0, 0.0)), (assets["car"],)),
        systems=(physics, update_graphics, platform_collision))

    platform = toyblock.Pool(
        8,
        (Body, Platform, Collision, PlatformSprite),
        (None, None, None, (assets["block"],)),
        systems=(physics, update_platform, collision)
    )

    @platform.init
    def init_platform(entity):
        size = 4
        entity[Platform].size = size
        collision = entity[Collision]
        collision.width = size*8.0
        collision.height = 8.0
