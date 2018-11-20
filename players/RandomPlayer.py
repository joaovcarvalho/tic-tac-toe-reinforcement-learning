import random

import numpy as np

import Game
from players.Player import Player


class RandomPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def take_action(self, game: Game):
        empty_cells = np.where(game.state == 0)

        if len(empty_cells[0]) == 0:
            print('No Empty cell')
            return

        x_empty, y_empty = empty_cells
        random_int = random.randint(0, len(x_empty) - 1)
        i = x_empty[random_int]
        j = y_empty[random_int]

        game.state[i, j] = self.symbol