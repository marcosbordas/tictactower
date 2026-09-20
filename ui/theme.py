import os

from kivy.metrics import sp

BG_TOP = (0.024, 0.031, 0.055, 1)
BG_BOTTOM = (0.045, 0.075, 0.145, 1)
CARD = (0.058, 0.088, 0.155, 1)
CARD_SOFT = (0.09, 0.125, 0.205, 1)
BORDER = (0.14, 0.24, 0.40, 1)

CYAN = (0.16, 0.78, 1.00, 1)
CYAN_DIM = (0.08, 0.45, 0.80, 1)
MAGENTA = (1.00, 0.36, 0.70, 1)
VIOLET = (0.62, 0.46, 1.00, 1)
GOLD = (1.00, 0.82, 0.25, 1)
GOOD = (0.32, 0.92, 0.64, 1)

X_COLOR = CYAN
O_COLOR = MAGENTA

TEXT = (0.93, 0.96, 1.00, 1)
MUTED = (0.58, 0.68, 0.85, 1)

FONT_UI = 'assets/fonts/Audiowide-Regular.ttf'
FONT_BODY = 'Roboto'

_POSSIBLE_FONT_UI = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fonts', 'Audiowide-Regular.ttf'),
    FONT_UI,
)
for _path in _POSSIBLE_FONT_UI:
    if os.path.isfile(_path):
        FONT_UI = _path
        break

TITLE_SIZE = sp(38)
SUB_SIZE = sp(15)
BODY_SIZE = sp(14)
SMALL_SIZE = sp(12)


def fade(color, alpha):
    return color[0], color[1], color[2], alpha


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(4))