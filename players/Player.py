import random

import numpy as np

import Game


class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.V = []

    def take_action(self, game: Game):
        raise NotImplemented

    def set_initial_v(self, game, triplets):
        value_function = np.zeros(game.num_states)
        for state, winner, ended in triplets:
            if ended:
                if winner == self.symbol:
                    v = 1
                else:
                    v = 0
            else:
                v = 0.5
            value_function[state] = v
        self.V = value_function

    def update_state_history(self, state):
        pass

    def learn(self, game: Game):
        pass

    def get_random_action(self, game):
        empty_cells = game.get_empty_cells()

        if len(empty_cells[0]) == 0:
            print('No Empty cell')
            return

        random_int = random.randint(0, len(empty_cells) - 1)
        return empty_cells[random_int]
