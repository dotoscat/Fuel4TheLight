from pyglet.sprite import Sprite
import toyblock
from components import Body, Platform, PlatformSprite

@toyblock.system
def physics(system, entity, dt, gravity):
    body = entity[Body]
    body.update(dt, gravity)

@toyblock.system
def graphics(system, entity):
    body = entity[Body]
    entity[Sprite].set_position(body.x, body.y)

@toyblock.system
def platform(system, entity):
    body = entity[Body]
    platform = entity[PlatformSprite]
    platform.x = body.x
    platform.y = body.y
    platform.times = entity[Platform].size
