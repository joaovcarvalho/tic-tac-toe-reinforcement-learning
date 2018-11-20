import numpy as np

from players import Player

BOARD_SIZE = 3
EMPTY_VALUE = 0


def get_cell_repr(value):
    return 'x' if value == 1 else 'o'


class Game:
    def __init__(self):
        self._state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.uint8)
        self.winner = None
        self.x = 1
        self.o = 2
        self.num_states = 3 ** (BOARD_SIZE * BOARD_SIZE)
        self.ended = False

    def clear_board(self):
        self._state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.uint8)

    def draw_board(self):
        print('=' * 12)
        for i in range(self._state.shape[0]):
            line = self._state[i]
            line_repr = ''
            for j in range(len(line)):
                cell = self._state[i][j]
                cell_repr = '_' if cell == EMPTY_VALUE else get_cell_repr(cell)
                line_repr += f'{cell_repr} | '
            print(line_repr)
        print('=' * 12)

    def reward(self, player: Player):
        if not self.is_game_over:
            return 0

        return 1 if player.symbol == self.winner else 0

    @property
    def state(self) -> np.ndarray:
        return self._state

    @property
    def state_number(self):
        k = 0
        h = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell = self.state[i , j]
                if cell == EMPTY_VALUE:
                    v = 0
                elif cell == 1:
                    v = 1
                elif cell == 2:
                    v = 2
                else:
                    raise ValueError('Cell with invalid value')
                h += (3**k) * v
                k += 1

        return h

    def get_empty_cells(self):
        empty_cells_tuple = np.where(self._state == 0)
        return list(zip(empty_cells_tuple[0], empty_cells_tuple[1]))

    def is_game_over(self, force_recalculate=False):
        if not force_recalculate:
            return self.ended

        has_empty_cells = EMPTY_VALUE in self._state
        self.winner = None

        # Check lines
        for i in range(self._state.shape[0]):
            line = self._state[i]
            possible_values = set(line)
            is_completed = len(possible_values) == 1 and EMPTY_VALUE not in possible_values
            if is_completed:
                self.winner = possible_values.pop()

        # Check columns
        for column in range(self._state.shape[1]):
            possible_values = set(self._state[:, column])
            is_completed = len(possible_values) == 1 and EMPTY_VALUE not in possible_values
            if is_completed:
                self.winner = possible_values.pop()

        # Todo improve this to be more generic
        first_diagonal = {self._state[0][0], self._state[1][1], self._state[2][2]}
        second_diagonal = {self._state[0][2], self._state[1][1], self._state[2][0]}

        for possible_values in [first_diagonal, second_diagonal]:
            is_completed = len(possible_values) == 1 and EMPTY_VALUE not in possible_values
            if is_completed:
                self.winner = possible_values.pop()

        self.ended = self.winner is not None or not has_empty_cells
        return self.ended
