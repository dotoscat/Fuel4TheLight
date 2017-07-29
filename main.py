#!/usr/bin/env python

import pyglet
import toyblock

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

class Body:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0

    def update(self, dt):
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt

@toyblock.system
def physics(system, entity, dt):
    entity[Body].update(dt)

if __name__ == "__main__":
    class GameWindow(pyglet.window.Window):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def on_draw(self):
            self.clear()

    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
    game_window = GameWindow(caption="Fuel4TheLight")
    icon = (pyglet.image.Texture.create_for_size(assets["car"].target, 16, 16).
            get_image_data())
    game_window.set_icon(icon)

    car_pool = toyblock.Pool(1, (Body,), systems=(physics,))
    pyglet.clock.schedule(physics)

    car = car_pool.get()

    pyglet.app.run()
