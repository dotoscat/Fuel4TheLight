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
        def __init__(self, label, action, x, y):
            self._x = x
            self._y = y
            self.label = label
            self._action = action

        def __call__(self, menu):
            self._action(menu)

    def __init__(self, cursor_sprite, x=0., y=0.):
        cursor_sprite.x = x
        self._x = x
        self._y = y
        self._cursor = None
        self._cursor_sprite = cursor_sprite
        self._entry = []

    def add_entry(self, label, action, x, y):
        label.x = self._x + x
        label.y = self._y + y
        entry = Menu.Entry(label, action, x, y)
        self._entry.append(entry)
        if self._cursor is None and self._entry:
            self._cursor = 0
            self._cursor_sprite.y = self._entry[0].label.y

    def set_entry(self, position):
        if self._cursor is None or not 0 <= position < len(self._entry):
            return False
        self._cursor = position
        self._cursor_sprite.y = self._entry[self._cursor].label.y
        return True

    def move_up(self):
        if self._cursor is not None and self._cursor - 1 >= 0:
            self._cursor -= 1
            self._cursor_sprite.y = self._entry[self._cursor].label.y
            return True
        return False

    def move_down(self):
        if self._cursor is not None and self._cursor + 1 < len(self._entry):
            self._cursor += 1
            self._cursor_sprite.y = self._entry[self._cursor].label.y
            return True
        return False

    def execute(self):
        if self._cursor is None: return
        self._entry[self._cursor](self)

class FractionLabel(pyglet.text.Label):
    def __init__(self, width, filler, *args, **kwargs):
        super(FractionBar, self).__init__(*args, **kwargs)
        self._num = 0
        self._dem = 0
        self._width = 0
        self._filler = 0

    def set_num(self, num):
        self._num = num
        self.update()

    def set_dem(self, dem):
        self._dem = dem
        self.update()

    def update(self):
        self.text = "{:{filler}>{width}}/{:{filler}>{width}}"
            .format(self._num, self._dem, filler=self._filler, width=self._width)
