import numpy as np

import Game
from players.Player import Player


class AIPlayer(Player):
    def __init__(self, symbol, eps=0.1, alpha=0.5, verbose=False):
        super().__init__(symbol)
        self.eps = eps
        self.alpha = alpha
        self.state_history = []
        self.V = None
        self.verbose = verbose

    def set_value_function(self, v):
        self.V = v

    def reset_history(self):
        self.state_history = []

    def take_action(self, game: Game):
        random_number = np.random.rand()
        next_move = None
        if random_number < self.eps:
            if self.verbose:
                print('Taking random action')
            next_move = self.get_random_action(game)
        else:
            if self.verbose:
                print('Taking greedy action')

            best_value = -1
            empty_cells = game.get_empty_cells()
            possible_moves = np.zeros((Game.BOARD_SIZE, Game.BOARD_SIZE))

            for i, j in empty_cells:
                game.state[i, j] = self.symbol
                state_number = game.state_number
                game.state[i, j] = Game.EMPTY_VALUE
                possible_moves[i, j] = self.V[state_number]

                if self.V[state_number] > best_value:
                    best_value = self.V[state_number]
                    next_move = (i, j)

            if self.verbose:
                print(possible_moves)

        if next_move is None:
            raise ValueError('Could not find next_move')

        i, j = next_move
        game.state[i, j] = self.symbol

    def update_state_history(self, state_number):
        self.state_history.append(state_number)

    def learn(self, game):
        reward = game.reward(self)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()
