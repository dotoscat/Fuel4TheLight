import pyglet

class Bar:
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
