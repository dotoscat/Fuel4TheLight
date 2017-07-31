from pyglet.sprite import Sprite
import toyblock
from .system import update_graphics, physics, update_platform,\
    update_collision, platform_collision, update_platform_sprite
from .components import Body, PlatformSprite, FloorCollision, Collision

def create(assets):
    global car
    global platform
    car = toyblock.Pool(
        1,
        (Body, FloorCollision, Sprite),
        ((True,), (*(0.0, 0.0), *(8.0, 0.0)), (assets["car"],)),
        systems=(physics, update_graphics, platform_collision))

    platform = toyblock.Pool(
        32,
        (Body, Collision, PlatformSprite),
        (None, None, (assets["block"],)),
        systems=(physics, update_platform, update_collision, update_platform_sprite)
    )
