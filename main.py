#!/usr/bin/env python

import pyglet

assets_list = {
    "car": "car.png",
    "block": "block.png",
}

if __name__ == "__main__":
    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    assets = {key : pyglet.resource.image(assets_list[key]) for key in assets_list}
