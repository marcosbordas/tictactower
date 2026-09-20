from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

from ui import theme


class BoardWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = None
        self.on_move = None
        self.bind(size=self.redraw, pos=self.redraw)

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
            self._draw_background(left, bottom, side)
            self._draw_highlights(game, left, bottom, cell)
            self._draw_grid(left, bottom, side, cell)
            self._draw_marks(game, left, bottom, cell)
            self._draw_mini_victories(game, left, bottom, cell)
            self._draw_macro_victory(game, left, bottom, cell)

    def _draw_background(self, left, bottom, side):
        Color(*theme.BG)
        Rectangle(pos=self.pos, size=self.size)
        Color(*theme.CARD)
        RoundedRectangle(pos=(left, bottom), size=(side, side), radius=[side * 0.01])

    def _draw_highlights(self, game, left, bottom, cell):
        for bi in range(9):
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            if not game.mini_available(bi):
                if game.macro[bi]:
                    color = theme.X_COLOR if game.macro[bi] == 'X' else theme.O_COLOR
                    Color(*theme.switch_color(color, 0.15))
                    RoundedRectangle(pos=(bx, by), size=(3 * cell, 3 * cell), radius=[cell * 0.12])
                continue
            if game.active_board == bi:
                Color(*theme.switch_color(theme.ACCENT, 0.18))
            elif game.active_board is None:
                Color(*theme.switch_color(theme.ACCENT, 0.07))
            else:
                continue
            RoundedRectangle(pos=(bx, by), size=(3 * cell, 3 * cell), radius=[cell * 0.12])

    def _draw_grid(self, left, bottom, side, cell):
        for i in range(10):
            x = left + i * cell
            y = bottom + i * cell
            if i % 3 == 0:
                Color(*theme.GRID)
                Line(points=[x, bottom, x, bottom + side], width=dp(2.4))
                Line(points=[left, y, left + side, y], width=dp(2.4))
            else:
                Color(*theme.GRID_SUB)
                Line(points=[x, bottom, x, bottom + side], width=dp(0.8))
                Line(points=[left, y, left + side, y], width=dp(0.8))

    def _draw_marks(self, game, left, bottom, cell):
        for bi, board in enumerate(game.boards):
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            for r in range(3):
                for c in range(3):
                    ch = board[r][c]
                    if not ch:
                        continue
                    self._draw_mark(ch, bx + c * cell, by + (2 - r) * cell, cell)

    def _draw_mark(self, ch, x, y, cell):
        inset = cell * 0.24
        stroke = max(cell * 0.13, dp(2.5))
        if ch == 'X':
            Color(*theme.X_COLOR)
            Line(points=[x + inset, y + inset, x + cell - inset, y + cell - inset],
                 width=stroke, cap='round')
            Line(points=[x + cell - inset, y + inset, x + inset, y + cell - inset],
                 width=stroke, cap='round')
        else:
            Color(*theme.O_COLOR)
            Line(circle=(x + cell / 2, y + cell / 2, cell / 2 - inset), width=stroke)

    def _draw_mini_victories(self, game, left, bottom, cell):
        for bi in range(9):
            line = game.mini_winner_line(bi)
            if not line:
                continue
            bx = left + (bi % 3) * 3 * cell
            by = bottom + (bi // 3) * 3 * cell
            p1 = self._mini_center(bx, by, line[0], cell)
            p2 = self._mini_center(bx, by, line[2], cell)
            Color(*theme.switch_color(theme.GOLD, 0.95))
            Line(points=[p1[0], p1[1], p2[0], p2[1]], width=cell * 0.16, cap='round')

    def _draw_macro_victory(self, game, left, bottom, cell):
        line = game.macro_winner_line()
        if not line:
            return
        centers = []
        for idx in line:
            cx = left + (idx % 3) * 3 * cell + cell * 1.5
            cy = bottom + (idx // 3) * 3 * cell + cell * 1.5
            centers.append((cx, cy))
        Color(*theme.GOLD)
        Line(points=[centers[0][0], centers[0][1], centers[2][0], centers[2][1]],
             width=cell * 0.22, cap='round')

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