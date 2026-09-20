from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from ui import theme


def attach_background(widget):
    bg = SolidBackground()
    widget.add_widget(bg)
    widget.bind(size=lambda *_: setattr(bg, 'size', (widget.width, widget.height)))
    bg.size = widget.size


class SolidBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*theme.BG_TOP)
            Rectangle(pos=self.pos, size=self.size)


class NeonButton(Widget):
    text = StringProperty('')
    primary = BooleanProperty(False)
    small = BooleanProperty(False)

    def __init__(self, **kwargs):
        self._pressed = False
        super().__init__(**kwargs)
        self._label = Label(valign='center', halign='center')
        self.add_widget(self._label)
        self.bind(pos=self._redraw, size=self._redraw, text=self._redraw,
                  primary=self._redraw, small=self._redraw)
        self._redraw()

    def _redraw(self, *_):
        self._label.text = self.text
        self._label.size = self.size
        self._label.pos = self.pos
        self._label.font_name = theme.FONT_UI
        self._label.font_size = sp(16) if not self.small else sp(12)
        self._label.outline_width = 1
        self._label.outline_color = (0, 0, 0, 0.55)
        radius = (dp(12),) * 4
        fill = theme.CYAN if self.primary else theme.CARD_SOFT
        if self._pressed:
            fill = theme.mix(fill, theme.TEXT, 0.16)
        border = theme.CYAN if self.primary else theme.BORDER
        self._label.color = theme.BG_TOP if self.primary else theme.TEXT
        canvas = self.canvas
        canvas.clear()
        g = dp(1.2)
        glow = theme.fade(border, 0.35 if not self.primary else 0.28)
        for i in (3, 2, 1):
            Color(*glow)
            Line(rounded_rectangle=[self.x - g * i, self.y - g * i,
                                    self.width + g * 2 * i, self.height + g * 2 * i,
                                    radius[0] + g * i, radius[1] + g * i,
                                    radius[2] + g * i, radius[3] + g * i],
                 width=dp(0.8))
        Color(*fill)
        RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        Color(*border)
        Line(rounded_rectangle=[self.x, self.y, self.width, self.height,
                                radius[0], radius[1], radius[2], radius[3]],
             width=dp(1.4))
        self._label.outline_width = 1

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._pressed = True
            self._redraw()
            return True
        return False

    def on_touch_up(self, touch):
        if not self._pressed:
            return False
        self._pressed = False
        self._redraw()
        if self.collide_point(*touch.pos):
            self.dispatch('on_release')
        return True

    def on_release(self):
        pass


class NeonToggle(NeonButton):
    selected = BooleanProperty(False)

    def _redraw(self, *_):
        self.primary = self.selected
        super()._redraw()


class NeonPill(Widget):
    text = StringProperty('')
    tint = ListProperty(theme.CYAN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._label = Label(valign='center', halign='center')
        self.add_widget(self._label)
        self.bind(pos=self._redraw, size=self._redraw, text=self._redraw,
                  tint=self._redraw)
        self._redraw()

    def _redraw(self, *_):
        self._label.text = self.text
        self._label.size = self.size
        self._label.pos = self.pos
        self._label.font_name = theme.FONT_UI
        self._label.font_size = sp(14)
        self._label.color = self.tint
        radius = ((self.height / 2),) * 4
        canvas = self.canvas
        canvas.clear()
        Color(*theme.fade(self.tint, 0.12))
        RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        Color(*theme.fade(self.tint, 0.75))
        Line(rounded_rectangle=[self.x, self.y, self.width, self.height,
                                radius[0], radius[1], radius[2], radius[3]],
             width=dp(1.2))