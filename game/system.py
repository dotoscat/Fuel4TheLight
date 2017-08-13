import pyglet
from pyglet.sprite import Sprite
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl
import toyblock
from .components import (Body, PlatformSprite, FloorCollision,
    Collision, Input, Type)
from .hud import Bar

class GameWindow(pyglet.window.Window):
    VWIDTH = 240
    VHEIGHT = 160

    @property
    def batch(self):
        return self._batch

    @property
    def layer(self):
        return self._layers

    def __init__(self, assets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fuel = Bar(8, GameWindow.VHEIGHT - 16, 64, 8, (0, 128, 255, 255), (0, 255, 128, 255))
        self._batch = pyglet.graphics.Batch()
        self._layers = [pyglet.graphics.OrderedGroup(i) for i in range(3)]
        self._darkness = [
            Sprite(assets["darkness"], i*8., -4., batch=self._batch, group=self._layers[2])
            for i in range(GameWindow.VWIDTH//8)
        ]

    def set_fuel(self, amount, max_amount):
        self._fuel.set_value(amount, max_amount)

    def on_draw(self):
        self.clear()
        self._batch.draw()
        self._fuel.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, GameWindow.VWIDTH, 0, GameWindow.VHEIGHT, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)

@toyblock.system
def input_sys(system, entity, game_state):
    input_ = entity[Input]
    body = entity[Body]
    floor_collision = entity[FloorCollision]

    if input_.left:
        body.vel_x = -Body.SPEED
    if input_.right:
        body.vel_x = Body.SPEED
    if not input_.left and not input_.right and body.vel_x != 0.0:
        body.vel_x = 0.0
    # print(input_.jump, input_.jump_pressed, input_._jumps)
    if input_.jump and input_.jump_pressed and floor_collision.touch_floor:
        floor_collision.touch_floor = False
        body.vel_y = Body.JUMP
        body.gravity = True
        input_._jumps -= 1
        game_state.decrease_fuel(5.)
    elif (input_.jump and input_.jump_pressed
        and not floor_collision.touch_floor and input_._jumps > 0):
        body.vel_y = Body.JUMP/1.5
        input_._jumps -= 1
        game_state.decrease_fuel(2.5)
    elif not input_._jump and body.vel_y > 0.0:
        body.vel_y = 0.
    input_.jump_pressed = False
    if floor_collision.touch_floor:
        input_.reset_jumps()

@toyblock.system
def physics(system, entity, dt, gravity):
    body = entity[Body]
    body.update(dt, gravity)

@toyblock.system
def update_graphics(system, entity):
    body = entity[Body]
    entity[Sprite].set_position(body.x, body.y)

@toyblock.system
def recycle(system, entity):
    if entity[Body].y + 16. < 0.0: entity.free()

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

def player_powerup(player, powerup, game_state):
    powerup.free()
    game_state.increase_fuel()

collision_t = {
    (Type.PLAYER, Type.POWERUP): player_powerup
}

@toyblock.system
def do_collision(system, entity, game_state):
    entities = system.entities
    entity_collision = entity[Collision]
    for sysentity in entities:
        #3prin
        if sysentity == entity: continue
        sysentity_collision = sysentity[Collision]
        #print(entity_collision.x, entity_collision.y, sysentity_collision.x, sysentity_collision.y)
        if not (entity_collision.intersects(sysentity_collision)
            and entity_collision.collides_with & sysentity_collision.type
            == sysentity_collision.type): continue
        collision_t[(entity_collision.type, sysentity_collision.type)](entity, sysentity, game_state)

@toyblock.system
def platform_collision(system, entity, platforms):
    body = entity[Body]
    floor_collision = entity[FloorCollision]
    if floor_collision.touch_floor:
        platform_collision = floor_collision.platform[Collision]
        body.y = floor_collision.platform[Body].y + 8.
        points = floor_collision.get_points(body.x, body.y)
        #if (points[0] in platform_collision or points[1] in platform_collision):
        #    return
    points = floor_collision.get_points(body.x, body.y)
    body.gravity = True
    floor_collision.touch_floor = False
    for platform in platforms:
        platform_collision = platform[Collision]
        if (body.vel_y > 0.0 or
        (points[0] not in platform_collision and
        points[1] not in platform_collision)):
            continue
        body.y = platform_collision.top
        body.vel_y = 0.0
        body.gravity = False
        floor_collision.touch_floor = True
        floor_collision.platform = platform
        break

def do(dt, gravity, game_state):
    input_sys(game_state)
    physics(dt, gravity)
    recycle()
    update_collision()
    platform_collision(game_state.platforms)
    do_collision(game_state)
    update_platform_sprite()
    update_graphics()
