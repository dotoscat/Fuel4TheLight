#!/usr/bin/env python

import pyglet

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

if __name__ == "__main__":
    class GameWindow(pyglet.window.Window):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = GameWindow(caption="Fuel4TheLight")
    icon = pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).get_image_data()
    game_window.set_icon(icon)

    pyglet.app.run()
