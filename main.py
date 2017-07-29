#!/usr/bin/env python

import pyglet
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl
import toyblock

class GameWindow(pyglet.window.Window):
        VWIDTH = 210
        VHEIGHT = 160
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sprites = []

        def on_draw(self):
            self.clear()
            for sprite in self.sprites:
                sprite.draw()

        def add_Sprite(self, Sprite_):
            self.sprites.append(Sprite_)

        def on_resize(self, width, height):
            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0, GameWindow.VWIDTH, 0, GameWindow.VHEIGHT, -1, 1)
            glMatrixMode(gl.GL_MODELVIEW)

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

if __name__ == "__main__":
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = GameWindow(caption="Fuel4TheLight")
    icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
            get_image_data())
    game_window.set_icon(icon)

    def do_systems(dt):
        physics(dt, -32.0)
        graphics()
        platform()

    pyglet.clock.schedule(do_systems)

    car = car_pool.get()
    game_window.add_Sprite(car[Sprite])
    car[Body].x = 64.0
    car[Body].y = 64.0
    game_window.push_handlers(car[Body])

    a_platform = platform_pool.get()
    game_window.add_Sprite(a_platform[PlatformSprite])
    a_platform[Body].x = 32
    a_platform[Body].y = 32

    pyglet.app.run()
