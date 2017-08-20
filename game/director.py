import pyglet
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl

director = None
_escenes = {}


class Director(pyglet.window.Window):

    director = None
    _scenes = {}

    def add_scene(key, scene):
        Director._scenes[key] = scene

    def set_scene(key):
        if Director.director is None: return
        Director.director.scene = Director._scenes[key]

    def __init__(self, *args, vwidth=None, vheight=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.vwidth = vwidth
        self.vheight = vheight
        self._scene = None
        Director.director = self

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if self._scene is not None:
            self.remove_handlers(self._scene)
            self._scene.quit()
            pyglet.clock.unschedule(self._scene.update)
        self._scene = scene
        self.push_handlers(scene)
        pyglet.clock.schedule(scene.update)
        scene.init()

    def on_draw(self):
        self.clear()
        if self._scene is not None:
            self._scene.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        width = self.vwidth if self.vwidth is not None else width
        height = self.vheight if self.vheight is not None else height
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)
