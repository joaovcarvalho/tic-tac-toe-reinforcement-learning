from Game import Game
from players.AIPlayer import AIPlayer
from value_function import get_state_hash_and_winner


def play_game(p1, p2, game: Game, draw_board=False):
    current_player = None
    while not game.is_game_over(force_recalculate=True):
        current_player = p2 if current_player == p1 else p1

        if draw_board:
            game.draw_board()

        current_player.take_action(game)
        state = game.state_number
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw_board:
        game.draw_board()
        print('Game Over')

    p1.learn(game)
    p2.learn(game)


game = Game()
player1 = AIPlayer(1)

all_possible_states = get_state_hash_and_winner(game)
player1.set_initial_v(game, all_possible_states)

player2 = AIPlayer(2)
player2.set_initial_v(game, all_possible_states)

NUM_EPISODES = 20000
for i in range(NUM_EPISODES):
    if i % 200 == 0:
        print(i)
    play_game(player1, player2, Game())

game = Game()
player1.verbose = True
player2.verbose = True
play_game(player1, player2, game, draw_board=True)
