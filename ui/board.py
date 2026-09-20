import math
import time

from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

from ui import theme


class BoardWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = None
        self.on_move = None
        self.last_move = None
        self._last_ts = 0.0
        self._pulse = 0.0
        self._clock = None
        self.bind(size=self.redraw, pos=self.redraw)

    def set_running(self, running):
        if running and self._clock is None:
            self._clock = Clock.schedule_interval(self._tick, 1 / 30)
        elif not running and self._clock is not None:
            self._clock.cancel()
            self._clock = None
        self.redraw()

    def _tick(self, dt):
        self._pulse = (self._pulse + dt) % 1.0
        if self.get_root_window() is None:
            return
        self.redraw()

    def mark(self, move):
        self.last_move = move
        self._last_ts = time.monotonic()

    def redraw(self, *_):
        self.canvas.clear()
        game = self.game
        if game is None:
            return
        width, height = self.size
        if width < 40 or height < 40:
            return
        pad = width * 0.02
        side = min(width, height) - pad * 2
        left = self.x + (width - side) / 2
        bottom = self.y + (height - side) / 2
        cell = side / 9.0
        with self.canvas:
            self._background()
            self._card(left, bottom, side)
            self._overlays(game, left, bottom, cell)
            self._grid(left, bottom, side, cell)
            self._marks(game, left, bottom, cell)
            self._last_move_ring(left, bottom, cell)
            self._playable_glow(game, left, bottom, cell)
            self._mini_wins(game, left, bottom, cell)
            self._macro_win(game, left, bottom, cell)

    def _background(self):
        Color(*theme.BG_TOP)
        Rectangle(pos=self.pos, size=self.size)

    def _card(self, left, bottom, side):
        Color(*theme.fade(theme.CARD, 0.92))
        RoundedRectangle(pos=(left, bottom), size=(side, side),
                         radius=[side * 0.016])
        Color(*theme.fade(theme.BORDER, 0.5))
        r = side * 0.016
        Line(rounded_rectangle=[left, bottom, side, side, r, r, r, r],
             width=dp(1.2))

    def _overlays(self, game, left, bottom, cell):
        for bi in range(9):
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            size = 3 * cell
            won = game.macro[bi]
            if won:
                color = theme.X_COLOR if won == 'X' else theme.O_COLOR
                Color(*theme.fade(color, 0.10))
                RoundedRectangle(pos=(bx, by), size=(size, size),
                                 radius=[cell * 0.12])
                continue
            if game.active_board == bi:
                continue
            if game.mini_available(bi) and game.active_board is not None:
                Color(*theme.fade(theme.BG_TOP, 0.24))
            else:
                Color(*theme.fade(theme.BG_TOP, 0.42))
            RoundedRectangle(pos=(bx, by), size=(size, size),
                             radius=[cell * 0.12])

    def _grid(self, left, bottom, side, cell):
        for i in range(10):
            x = left + i * cell
            y = bottom + i * cell
            vertical = (x, bottom, x, bottom + side)
            horizontal = (left, y, left + side, y)
            if i % 3 == 0:
                Color(*theme.fade(theme.CYAN_DIM, 0.14))
                Line(points=vertical, width=dp(6.0))
                Line(points=horizontal, width=dp(6.0))
                Color(*theme.fade(theme.CYAN_DIM, 0.9))
                Line(points=vertical, width=dp(1.8))
                Line(points=horizontal, width=dp(1.8))
            else:
                Color(*theme.fade(theme.BORDER, 0.55))
                Line(points=vertical, width=dp(0.9))
                Line(points=horizontal, width=dp(0.9))

    def _marks(self, game, left, bottom, cell):
        for bi, board in enumerate(game.boards):
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            for r in range(3):
                for c in range(3):
                    ch = board[r][c]
                    if ch:
                        self._draw_mark(ch, bx + c * cell, by + (2 - r) * cell, cell)

    def _draw_mark(self, ch, x, y, cell):
        inset = cell * 0.22
        stroke = max(cell * 0.14, dp(2.0))
        if ch == 'X':
            color = theme.X_COLOR
        else:
            color = theme.O_COLOR
        Color(*theme.fade(color, 0.16))
        glow = stroke * 2.8
        if ch == 'X':
            Line(points=[x + inset, y + inset, x + cell - inset, y + cell - inset],
                 width=glow, cap='round')
            Line(points=[x + cell - inset, y + inset, x + inset, y + cell - inset],
                 width=glow, cap='round')
        else:
            Line(circle=(x + cell / 2, y + cell / 2, cell / 2 - inset),
                 width=glow)
        Color(*color)
        if ch == 'X':
            Line(points=[x + inset, y + inset, x + cell - inset, y + cell - inset],
                 width=stroke, cap='round')
            Line(points=[x + cell - inset, y + inset, x + inset, y + cell - inset],
                 width=stroke, cap='round')
        else:
            Line(circle=(x + cell / 2, y + cell / 2, cell / 2 - inset),
                 width=stroke)

    def _last_move_ring(self, left, bottom, cell):
        move = self.last_move
        if not move or not self.game or self.game.game_result() is not None:
            return
        if not self.game.boards[move[0]][move[1]][move[2]]:
            self.last_move = None
            return
        dt = time.monotonic() - self._last_ts
        if dt > 1.1:
            self.last_move = None
            return
        alpha = max(0.0, 0.8 - dt * 0.75)
        bi, r, c = move
        bx = left + (bi % 3) * 3 * cell
        by = bottom + (bi // 3) * 3 * cell
        cx = bx + c * cell + cell / 2
        cy = by + (2 - r) * cell + cell / 2
        Color(*theme.fade(theme.GOLD, alpha))
        Line(circle=(cx, cy, cell / 2 - cell * 0.14),
             width=dp(2.2))

    def _playable_glow(self, game, left, bottom, cell):
        if game.game_result() is not None:
            return
        if game.active_board is not None and game.mini_available(game.active_board):
            targets = (game.active_board,)
            soft = False
        else:
            targets = [bi for bi in range(9) if game.mini_available(bi)]
            soft = True
        wave = 0.5 + 0.3 * math.sin(self._pulse * math.tau)
        for bi in targets:
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            size = 3 * cell
            inset = cell * 0.06
            x = bx + inset
            y = by + inset
            w = size - inset * 2
            alpha = (0.30 + 0.18 * wave) if soft else (0.55 + 0.25 * wave)
            Color(*theme.fade(theme.CYAN, alpha))
            radius = cell * 0.14
            for i in range(3):
                g = (i + 1) * dp(1.6)
                Color(*theme.fade(theme.CYAN, alpha * (0.35 - i * 0.1)))
                Line(rounded_rectangle=[x - g, y - g, w + g * 2, w + g * 2,
                                        radius + g, radius + g, radius + g, radius + g],
                     width=dp(1.4))
            Color(*theme.fade(theme.CYAN, alpha))
            Line(rounded_rectangle=[x, y, w, w,
                                    radius, radius, radius, radius],
                 width=dp(2.2))

    def _mini_wins(self, game, left, bottom, cell):
        for bi in range(9):
            line = game.mini_winner_line(bi)
            if not line:
                continue
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            p1 = self._mini_center(bx, by, line[0], cell)
            p2 = self._mini_center(bx, by, line[2], cell)
            Color(*theme.fade(theme.GOLD, 0.18))
            Line(points=[p1[0], p1[1], p2[0], p2[1]],
                 width=cell * 0.34, cap='round')
            Color(*theme.fade(theme.GOLD, 0.95))
            Line(points=[p1[0], p1[1], p2[0], p2[1]],
                 width=cell * 0.14, cap='round')

    def _macro_win(self, game, left, bottom, cell):
        line = game.macro_winner_line()
        if not line:
            return
        centers = []
        for idx in line:
            cx = left + (idx % 3) * 3 * cell + cell * 1.5
            cy = bottom + (idx // 3) * 3 * cell + cell * 1.5
            centers.append((cx, cy))
        Color(*theme.fade(theme.GOLD, 0.16))
        Line(points=[centers[0][0], centers[0][1], centers[2][0], centers[2][1]],
             width=cell * 0.5, cap='round')
        Color(*theme.GOLD)
        Line(points=[centers[0][0], centers[0][1], centers[2][0], centers[2][1]],
             width=cell * 0.2, cap='round')

    def _mini_center(self, bx, by, idx, cell):
        r = idx // 3
        c = idx % 3
        return bx + c * cell + cell / 2, by + (2 - r) * cell + cell / 2

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if self.game is None or self.game.game_result() is not None:
            return True
        width, height = self.size
        pad = width * 0.02
        side = min(width, height) - pad * 2
        left = (width - side) / 2
        bottom = (height - side) / 2
        cell = side / 9.0
        x = touch.x - self.x
        y = touch.y - self.y
        if not (left <= x < left + side and bottom <= y < bottom + side):
            return True
        col = int((x - left) // cell)
        row_from_bottom = int((y - bottom) // cell)
        if not (0 <= col < 9 and 0 <= row_from_bottom < 9):
            return True
        outer_col = col // 3
        outer_row = 2 - (row_from_bottom // 3)
        bi = outer_row * 3 + outer_col
        c = col % 3
        r = 2 - (row_from_bottom % 3)
        if (bi, r, c) in self.game.legal_moves():
            if self.on_move:
                self.on_move(bi, r, c)
        return True