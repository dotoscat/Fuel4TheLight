#!/usr/bin/env python

import pyglet
from pyglet.sprite import Sprite
import game.pool as pool
import game.system as system
from game.components import Body, Platform, PlatformSprite

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

def create_platform(x, y, pool, window, platforms):
    a_platform = pool.get()
    window.add_Sprite(a_platform[PlatformSprite])
    a_platform[Body].x = x
    a_platform[Body].y = y
    platforms.append(a_platform)

if __name__ == "__main__":
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = system.GameWindow(caption="Fuel4TheLight")
    icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
            get_image_data())
    game_window.set_icon(icon)

    platforms = []

    pyglet.clock.schedule(system.do, -160.0, platforms)

    pool.create(assets)

    car = pool.car.get()
    game_window.add_Sprite(car[Sprite])
    car[Body].x = 64.0
    car[Body].y = 64.0
    game_window.push_handlers(car[Body])

    create_platform(50.0, 32.0, pool.platform, game_window, platforms)
    create_platform(50.0, 72.0, pool.platform, game_window, platforms)

    pyglet.app.run()
