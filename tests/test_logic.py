import pytest

from game.logic import UltimateTicTacToe
from game.ai import choose_move, EASY, MEDIUM, HARD


def test_initial_state():
    game = UltimateTicTacToe()
    assert game.turn == 'X'
    assert game.active_board is None
    assert game.game_result() is None
    assert len(game.legal_moves()) == 81


def test_first_move_sets_active_board():
    game = UltimateTicTacToe()
    assert game.play(4, 0, 0)
    assert game.active_board == 0


def test_opponent_forced_into_sent_board():
    game = UltimateTicTacToe()
    game.play(4, 1, 1)
    assert game.turn == 'O'
    assert game.active_board == 4
    assert game.legal_moves() == [(4, r, c) for r in range(3) for c in range(3) if not (r == 1 and c == 1)]


def test_wrong_board_rejected():
    game = UltimateTicTacToe()
    game.play(4, 1, 1)
    assert not game.play(0, 0, 0)


def test_occupied_cell_rejected():
    game = UltimateTicTacToe()
    game.play(4, 0, 0)
    assert game.boards[4][0][0] == 'X'
    assert not game.play(4, 0, 0)


def test_mini_win_sets_macro_cell():
    game = UltimateTicTacToe()
    game.play(4, 0, 0)
    game.play(0, 1, 1)
    game.play(4, 0, 1)
    game.play(1, 1, 0)
    game.play(3, 0, 2)
    game.play(2, 1, 1)
    game.play(4, 0, 2)
    assert game.macro[4] == 'X'
    assert game.active_board == 2


def test_full_or_won_boards_unlock_free_move():
    game = UltimateTicTacToe()
    game.boards[0] = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', 'X']]
    assert not game.mini_available(0)
    game.play(1, 0, 0)
    assert game.active_board is None
    assert len(game.legal_moves()) > 9


def test_undo_restores_state_exactly():
    game = UltimateTicTacToe()
    for move in [(4, 0, 0), (0, 1, 1), (4, 0, 1)]:
        game.play(*move)
    game.undo()
    game.undo()
    game.undo()
    assert len(game.move_stack) == 0
    assert game.turn == 'X'
    assert game.active_board is None
    assert game.moves == 0


def test_macro_winner_detected():
    game = UltimateTicTacToe()
    game.macro = ['X', 'X', 'X', '', '', '', '', '', '']
    assert game.macro_winner() == 'X'
    assert game.game_result() == 'X'
    assert game.macro_winner_line() == (0, 1, 2)


@pytest.mark.parametrize('level', [EASY, MEDIUM, HARD])
def test_ai_always_returns_legal_moves(level):
    game = UltimateTicTacToe()
    for _ in range(4):
        move = choose_move(game, level)
        assert move in game.legal_moves()
        assert game.play(*move)
    assert game.game_result() is None