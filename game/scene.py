import pyglet

class Scene(object):
    """
        A scene will...
        1. Handle input,
        2. loop
        3. what to draw -> groups!
    """

    def __init__(self, n_groups):
        self._batch = pyglet.graphics.Batch()
        self._groups = [pyglet.graphics.OrderedGroup(i) for i in range(n_groups)]

    @property
    def batch(self):
        return self._batch

    @property
    def group(self):
        return self._groups

    def draw(self):
        self._batch.draw()

    def init(self):
        pass

    def quit(self):
        pass

    def update(self, dt):
        pass
