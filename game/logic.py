class UltimateTicTacToe:
    LINES = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.boards = [[[''] * 3 for _ in range(3)] for _ in range(9)]
        self.macro = [''] * 9
        self.turn = 'X'
        self.active_board = None
        self.move_stack = []
        self._snapshots = []

    @property
    def moves(self):
        return len(self.move_stack)

    @property
    def last_move(self):
        return self.move_stack[-1] if self.move_stack else None

    def mini_winner(self, bi):
        board = self.boards[bi]
        for line in self.LINES:
            values = [board[i // 3][i % 3] for i in line]
            if values[0] and values[0] == values[1] == values[2]:
                return values[0]
        return ''

    def mini_winner_line(self, bi):
        board = self.boards[bi]
        for line in self.LINES:
            values = [board[i // 3][i % 3] for i in line]
            if values[0] and values[0] == values[1] == values[2]:
                return line
        return None

    def mini_full(self, bi):
        return all(cell for row in self.boards[bi] for cell in row)

    def mini_available(self, bi):
        return self.macro[bi] == '' and not self.mini_full(bi)

    def macro_winner(self):
        for line in self.LINES:
            values = [self.macro[i] for i in line]
            if values[0] and values[0] == values[1] == values[2]:
                return values[0]
        return ''

    def macro_winner_line(self):
        for line in self.LINES:
            values = [self.macro[i] for i in line]
            if values[0] and values[0] == values[1] == values[2]:
                return line
        return None

    def game_result(self):
        winner = self.macro_winner()
        if winner:
            return winner
        if self.moves == 81:
            return 'D'
        return None

    def legal_moves(self):
        targets = range(9)
        if self.active_board is not None and self.mini_available(self.active_board):
            targets = (self.active_board,)
        moves = []
        for bi in targets:
            if not self.mini_available(bi):
                continue
            board = self.boards[bi]
            for r in range(3):
                for c in range(3):
                    if not board[r][c]:
                        moves.append((bi, r, c))
        return moves

    def play(self, bi, r, c):
        if not (0 <= bi < 9 and 0 <= r < 3 and 0 <= c < 3):
            return False
        if self.macro[bi] or self.boards[bi][r][c]:
            return False
        if self.active_board is not None and bi != self.active_board:
            return False
        self._snapshots.append((self.active_board, self.turn))
        self.boards[bi][r][c] = self.turn
        self.move_stack.append((bi, r, c))
        if self.mini_winner(bi):
            self.macro[bi] = self.turn
        self._switch_turn(r, c)
        return True

    def undo(self):
        if not self.move_stack:
            return
        bi, r, c = self.move_stack.pop()
        if self.macro[bi]:
            self.macro[bi] = ''
        self.boards[bi][r][c] = ''
        self.active_board, self.turn = self._snapshots.pop()

    def _switch_turn(self, r, c):
        self.turn = 'O' if self.turn == 'X' else 'X'
        next_board = r * 3 + c
        if self.mini_available(next_board):
            self.active_board = next_board
        else:
            self.active_board = None