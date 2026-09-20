import random

EASY = 'FACIL'
MEDIUM = 'MEDIO'
HARD = 'DIFICIL'


def choose_move(game, level):
    if game.game_result() is not None or not game.legal_moves():
        return None
    ai_char = game.turn
    human = 'O' if ai_char == 'X' else 'X'
    ordered = ordered_moves(game, ai_char, human)
    if level == EASY:
        if random.random() < 0.35:
            return ordered[0]
        return random.choice(ordered)
    depth = 2 if level == MEDIUM else 4
    results = []
    for move in ordered[:14]:
        game.play(*move)
        value = minimax(game, depth - 1, -float('inf'), float('inf'), False, ai_char, human)
        game.undo()
        results.append((value, move))
    results.sort(key=lambda item: item[0], reverse=True)
    best = results[0][0]
    candidates = [move for value, move in results if value == best]
    return random.choice(candidates)


def minimax(game, depth, alpha, beta, maximizing, ai_char, human):
    result = game.game_result()
    if result is not None:
        if result == 'D':
            return 0
        return 1000000 + depth if result == ai_char else -1000000 - depth
    if depth == 0:
        return evaluate(game, ai_char, human)
    moves = ordered_moves(game, ai_char, human)[:14]
    if maximizing:
        best = -float('inf')
        for move in moves:
            game.play(*move)
            value = minimax(game, depth - 1, alpha, beta, False, ai_char, human)
            game.undo()
            best = max(best, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best
    best = float('inf')
    for move in moves:
        game.play(*move)
        value = minimax(game, depth - 1, alpha, beta, True, ai_char, human)
        game.undo()
        best = min(best, value)
        beta = min(beta, value)
        if beta <= alpha:
            break
    return best


def evaluate(game, ai_char, human):
    winner = game.macro_winner()
    if winner == ai_char:
        return 10000000
    if winner == human:
        return -10000000
    score = 0
    for bi in range(9):
        mini_winner = game.mini_winner(bi)
        if mini_winner == ai_char:
            score += 500
        elif mini_winner == human:
            score -= 500
    for bi in range(9):
        if game.macro[bi]:
            continue
        board = game.boards[bi]
        for line in game.LINES:
            ai_count = 0
            human_count = 0
            for i in line:
                ch = board[i // 3][i % 3]
                if ch == ai_char:
                    ai_count += 1
                elif ch == human:
                    human_count += 1
            if ai_count and not human_count:
                score += ai_count * 12
            elif human_count and not ai_count:
                score -= human_count * 10
    return score


def ordered_moves(game, ai_char, human):
    scored = []
    for move in game.legal_moves():
        game.play(*move)
        scored.append((evaluate(game, ai_char, human), move))
        game.undo()
    scored.sort(key=lambda item: item[0], reverse=True)
    return [move for _, move in scored]