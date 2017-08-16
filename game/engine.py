from .scene import Scene
from pyglet.window import key

class Engine(Scene):
    def __init__(self):
        super().__init__()

    def on_key_press(key, mod):
        print(key, mod)
