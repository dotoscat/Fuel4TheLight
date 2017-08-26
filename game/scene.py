# Fuel4TheLight
# Copyright (C) 2017  Oscar Triano @cat_dotoscat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
