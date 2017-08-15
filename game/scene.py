import pyglet

class Scene(object):
    """
        A scene will...
        1. Handle input,
        2. loop
        3. what to draw -> layers
    """

    def __init__(self, n_layers):
        self._batch = pyglet.graphics.Batch()
        self._layers = [pyglet.graphics.OrderedGroup(i) for i in range(n_layers)]

    @property
    def batch(self):
        return self._batch

    @property
    def layer(self):
        return self._layers

    def draw(self):
        self._batch.draw()
