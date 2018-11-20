from Game import BOARD_SIZE


def get_state_hash_and_winner(game, i=0, j=0):
    results = []

    for v in (0, 1, 2):
        game.state[i, j] = v
        if j == BOARD_SIZE - 1:
            if i == BOARD_SIZE - 1:
                state = game.state_number
                ended = game.is_game_over(force_recalculate=True)
                winner = game.winner
                results.append((state, winner, ended))
            else:
                results.extend(
                    get_state_hash_and_winner(game, i + 1, 0)
                )
        else:
            results.extend(
                get_state_hash_and_winner(game, i, j + 1)
            )
    return results