from random import choice, randrange
from pyglet.window import key
from pyglet.sprite import Sprite
import pyglet
import toyblock
from .system import (update_graphics, physics, recycle,
    update_collision, platform_collision, update_platform_sprite, input_sys,
    do_collision)
from .system import do as do_systems
from .components import (Body, PlatformSprite, FloorCollision, Collision, Input)
from .scene import Scene
from . import constants
from .gui import Bar
from .constants import Type, S
from .director import Director

class Engine(Scene):

    RED = (255, 0, 0, 255)

    READY = 0
    RUNNING = 1
    PAUSED = 2
    GAME_OVER = 3

    def __init__(self, assets):
        super().__init__(3)
        self._pool = {
            "car": toyblock.Pool(
                1,
                (Input, Body, FloorCollision, Collision, Sprite),
                (None, (True,), (*(0.0, 0.0), *(8.0, 0.0)), None, (assets["car_left"],)),
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
        for key in self._pool:
            self._pool[key].clean(self._free)
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
        self._meters = 0.
        self._meters_label = pyglet.text.Label(
            text="0 meters",
            anchor_y="center",
            color=Engine.RED,
            x=constants.VWIDTH/2.,
            y=constants.VHEIGHT - S,
            batch=self.batch,
            group=self.group[2]
        )
        self._speed = constants.ENGINE_SPEED
        self._car = None
        self._car_input = None
        self._powerup = None
        self._game_over_label = pyglet.text.Label(
            text="GAME OVER",
            bold=True,
            anchor_x="center",
            anchor_y="center",
            x=constants.VWIDTH/2.,
            y=constants.VHEIGHT/2.,
            color=Engine.RED
        )
        self._paused_label = pyglet.text.Label(
            text="PAUSED",
            bold=True,
            anchor_x="center",
            anchor_y="center",
            x=constants.VWIDTH/2.,
            y=constants.VHEIGHT/2.,
            color=Engine.RED
        )
        self._ready_label = pyglet.text.Label(
            text="READY",
            bold=True,
            anchor_x="center",
            anchor_y="center",
            x=constants.VWIDTH/2.,
            y=constants.VHEIGHT/2.,
            color=Engine.RED
        )
        self._state = None
        self._sounds = {
            "second_jump": pyglet.media.StaticSource(assets["second_jump"]),
            "landing": pyglet.media.StaticSource(assets["landing"]),
            "fuel_pickup": pyglet.media.StaticSource(assets["fuel_pickup"])
        }
        self.assets = assets

    @property
    def sound(self):
        return self._sounds

    @property
    def platforms(self):
        return self._platforms

    def _free(self, entity):
        if entity.pool == self._pool["platform"]:
            entity[PlatformSprite].visible = False
            self._platforms.remove(entity)
        else:
            entity[Sprite].visible = False
        if entity == self._car:
            self._set_game_over()
            self._car = None
        if entity == self._powerup: self._powerup = None

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

    def create_car(self, x, y):
        car = self._pool["car"].get()
        car[Sprite].visible = True
        Engine._set_entity_component(car, Body, {"x": x, "y": y})
        collision = car[Collision]
        collision.width = 8.
        collision.height = 8.
        collision.type = Type.PLAYER
        collision.collides_with = Type.POWERUP
        self._car_input = car[Input]
        self._car = car

    def create_powerup(self, x, y):
        fuel = self._pool["powerup"].get()
        fuel[FloorCollision].reset()
        fuel[Sprite].visible = True
        Engine._set_entity_component(fuel, Body, {"x": x, "y": y, "vel_y": 0.})
        collision = fuel[Collision]
        collision.type = Type.POWERUP
        collision.width = 8.
        collision.height = 8.
        self._powerup = fuel

    def on_key_press(self, symbol, mod):
        if self._state == Engine.RUNNING and symbol == key.RETURN:
            self._state = Engine.PAUSED
        elif self._state == Engine.PAUSED and symbol == key.RETURN:
            self._state = Engine.RUNNING
        self._car_input.on_key_press(symbol, mod)

    def on_key_release(self, symbol, mod):
        self._car_input.on_key_release(symbol, mod)

    def increase_fuel(self, fuel=10.):
        self._fuel += fuel
        if self._fuel > self._MAX_FUEL:
            self._fuel = self._MAX_FUEL

    def decrease_fuel(self, fuel):
        self._fuel -= fuel
        if self._fuel < 0.:
            self._fuel = 0.

    def update(self, dt):
        if self._state != Engine.RUNNING: return

        if self._fuel <= 0:
            self._car.free() # Triggers Engine._free method

        self._distance += self._speed*dt
        self._meters += self._speed*dt/S
        if self._distance > constants.JUMP/4.:
            self._speed += 0.1
            self._generate_random_platform(constants.VHEIGHT + 8, -self._speed)
            for platform in self._platforms:
                platform[Body].vel_y = -self._speed
            self._distance = 0.
            if self._powerup is None and randrange(self._MAX_FUEL/4., self._MAX_FUEL) > self._fuel:
                self._generate_random_powerup()
        if self._car is not None and self._fuel > 0.0:
            if self._car[Body].vel_x > 0.0:
                self._fuel += -dt*2.
            else:
                self._fuel += -dt*1.
        do_systems(dt, self)

    def _generate_random_powerup(self):
        while True:
            platform = choice(self._platforms)
            if platform[Body].y <= constants.VHEIGHT/4. or platform == self._car[FloorCollision].platform:
                continue
            y = platform[Body].y + S*2.
            x = randrange(platform[Collision].x, platform[Collision].right - S)
            self.create_powerup(x, y)
            break

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

    def init(self):
        self.create_car(constants.VWIDTH/2., 16.)
        self.start()

    def quit(self):
        self._pool["platform"].free_all()
        self._pool["powerup"].free_all()
        self._powerup = None

    def _set_running(self, dt):
        self._state = Engine.RUNNING

    def _set_game_over(self):
        self._state = Engine.GAME_OVER

        def to_title(dt):
            Director.set_scene("title")

        pyglet.clock.schedule_once(to_title, 2.)

    def start(self):
        self._speed = constants.ENGINE_SPEED
        self._meters = 0
        self._fuel = self._MAX_FUEL
        self._state = Engine.READY
        self.create_platform(0., 0., constants.VWIDTH//8, -constants.ENGINE_SPEED)
        y = 8.0
        while y < constants.VHEIGHT:
            print(y)
            y += constants.VHEIGHT/4.
            self._generate_random_platform(y, -constants.ENGINE_SPEED)
        pyglet.clock.schedule_once(self._set_running, 2.)
        do_systems(0., self)

    def draw(self):
        super().draw()
        self._fuel_bar.set_value(self._fuel, self._MAX_FUEL)
        self._fuel_bar.draw()
        self._meters_label.text = str(int(self._meters)) + " meters"
        if self._state == Engine.PAUSED:
            self._paused_label.draw()
        if self._state == Engine.GAME_OVER:
            self._game_over_label.draw()
        if self._state == Engine.READY:
            self._ready_label.draw()
