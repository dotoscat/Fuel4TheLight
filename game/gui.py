import pyglet

class Bar(object):
    def __init__(self, x, y, width, height, fg, bg, margin=1.):
        """
            x, y, width and height are pixels
            fg: (r, g, b, a) #Foreground
            bg: (r, g, b, a) #Background
            margin: margin for the bar
        """
        self._fg = (pyglet.image.SolidColorImagePattern(fg)
            .create_image(width, height)
        )
        self._bg = (pyglet.image.SolidColorImagePattern(bg)
            .create_image(width, height)
        )
        print(self._fg)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._margin = margin
        self._value = 0.

    def set_value(self, value, max_value):
        """
            change the bar size, foreground, setting value and max_value.
        """
        self._value = value*(self._width-self._margin*2.)/max_value

    def draw(self):
        margin = self._margin
        self._bg.blit(self._x, self._y)
        self._fg.blit(
            self._x + margin, self._y + margin,
            width=self._value, height=self._height - margin*2.
        )

class Menu(object):

    class Entry(object):
        def __init__(self, text, action):
            self._action = action

        def __call__(self, menu):
            self._action(menu)

    def __init__(self, x=0., y=0., batch=None, group=None):
        self._x = 0.
        self._y = 0.
        self._cursor = 0
        self._sprite_cursor = None
        self._entry = []

    def move_up(self):
        if self._cursor - 1 >= 0:
            self._cursor -= 1
            return True
        return False

    def move_down(self):
        if self._cursor + 1 < len(self._entry):
            self._cursor += 1
            return True
        return False

    def execute(self):
        self._entry[self._cursor](self)
