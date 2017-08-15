import pyglet
from pyglet.gl import glViewport, glOrtho, glMatrixMode, glLoadIdentity
from pyglet import gl

class Director(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scene = None
        self.scene = scene

    @property
    def scene(self):
        return self._scene

    @scene.setter(self, scene):
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
        glOrtho(0, GameWindow.VWIDTH, 0, GameWindow.VHEIGHT, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)
        
