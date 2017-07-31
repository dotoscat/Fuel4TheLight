import pyglet
from pyglet.sprite import Sprite
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl
import toyblock
from .components import Body, PlatformSprite, FloorCollision, Collision

class GameWindow(pyglet.window.Window):
    VWIDTH = 210
    VHEIGHT = 160
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprites = []

    def on_draw(self):
        self.clear()
        #print("on draw")
        for sprite in self.sprites:
            #if isinstance(sprite, PlatformSprite):
            #    print("PlatformSprite", sprite.y + 8.)
            #else:
            #    print(sprite.y)
            sprite.draw()
        #print("end")

    def add_Sprite(self, Sprite_):
        self.sprites.append(Sprite_)

    def remove_Sprite(self, Sprite_):
        self.sprites.remove(Sprite_)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, GameWindow.VWIDTH, 0, GameWindow.VHEIGHT, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)

@toyblock.system
def physics(system, entity, dt, gravity):
    body = entity[Body]
    body.update(dt, gravity)

@toyblock.system
def update_graphics(system, entity):
    body = entity[Body]
    entity[Sprite].set_position(body.x, body.y)
    if body.touch_floor:
        entity_sprite = entity[Sprite]
        platform = entity[FloorCollision].platform
        platform_sprite = platform[PlatformSprite]
        print("update_graphics assert", platform_sprite.y + 8., entity_sprite.y)
        assert platform_sprite.y + 8. == entity_sprite.y
    print("update_graphics", body.y, entity[Sprite].y)

@toyblock.system
def update_platform(system, entity):
    if entity[Body].y + 8. < 0.0: entity.free()

@toyblock.system
def update_platform_sprite(system, entity):
    body = entity[Body]
    platform = entity[PlatformSprite]
    platform.x = body.x
    platform.y = body.y

@toyblock.system
def update_collision(system, entity):
    body = entity[Body]
    collision = entity[Collision]
    collision.x = body.x
    collision.y = body.y

@toyblock.system
def platform_collision(system, entity, platforms):
    body = entity[Body]
    floor_collision = entity[FloorCollision]
    if body.touch_floor:
        platform_collision = floor_collision.platform[Collision]
        print("Update platform collision 2 (1)", body.y, floor_collision.platform[Body].y + 8., entity[Sprite].y)
        body.y = floor_collision.platform[Body].y + 8.
        print("Update platform collision 2 (2)", body.y, floor_collision.platform[Body].y + 8, entity[Sprite].y)
        assert body.y == platform_collision.top
        points = floor_collision.get_points(body.x, body.y)
        if (points[0] in platform_collision or points[1] in platform_collision):
            return
        else:
            print("why?")
    print("Ahem...")
    points = floor_collision.get_points(body.x, body.y)
    for platform in platforms:
        platform_collision = platform[Collision]
        if (body.vel_y > 0.0 or
        (points[0] not in platform_collision and
        points[1] not in platform_collision)):
            # if body.vel_y > 0.0: print(body.vel_y)
            body.touch_floor = False
            body.gravity = True
            continue
        body.y = platform_collision.top
        body.vel_y = 0.0
        body.jumped = False
        body.gravity = False
        body.touch_floor = True
        floor_collision.platform = platform
        print("Wii")
        break

def do(dt, gravity, platforms, car2):
    physics(dt, gravity)
    update_platform()
    update_collision()
    platform_collision(platforms)
    update_platform_sprite()
    update_graphics()
    if len(platforms):
        car2.y = platforms[len(platforms)-1][PlatformSprite].y
        print("car2", car2.y)
