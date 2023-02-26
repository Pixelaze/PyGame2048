from random import randint


# Возможные значения направления хода
class Directions:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    DIRECTIONS_DICT = {
        "UP": UP,
        "DOWN": DOWN,
        "RIGHT": RIGHT,
        "LEFT": LEFT
    }


# Возможные статусы игры
class Status:
    WINNED = 0
    PLAYING = 1
    LOSED = 2


# Класс с игровым полем
class GameField:
    def __init__(self):
        self.field = [[None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None]]
        self.status = Status.PLAYING

    def add_piece(self):
        available_positions = []
        for x in range(4):
            for y in range(4):
                if self.field[x][y] is None:
                    available_positions.append((x, y))

        if len(available_positions) == 0:
            self.lose_game()
            return

        x, y = available_positions[randint(0, len(available_positions) - 1)]
        self.field[x][y] = 2

    def check_state(self):
        for i in range(4):
            for j in range(4):
                if self.field[i][j] >= 2048:
                    self.win_game()

        for x in range(4):
            for y in range(4):
                if self.field[x][y] is None:
                    return

        for x in range(3):
            if self.field[x][3] == [x + 1][3]:
                return
            if self.field[3][x] == self.field[x + 1][3]:
                return
            for y in range(3):
                if self.field[x][y] == self.field[x + 1][y] or self.field[x][y] == self.field[x][y + 1]:
                    return

        self.lose_game()

    # Соединяет клетки с пустыми
    def compress_field(self):
        is_changed = False

        compressed_field = []

        for x in range(4):
            compressed_field.append([None] * 4)

        for x in range(4):
            current_position = 0
            for y in range(4):
                if self.field[x][y] is not None:
                    compressed_field[x][current_position] = self.field[x][y]

                    if y != current_position:
                        is_changed = True

                    current_position += 1

        self.field = compressed_field.copy()
        return is_changed

    # Соединяет клетки с НЕ пустыми
    def merge_cells(self):
        is_changed = False

        for x in range(4):
            for y in range(3):
                if self.field[x][y] is not None and self.field[x][y] == self.field[x][y + 1]:
                    self.field[x][y] *= 2
                    self.field[x][y + 1] = None

                    is_changed = True

        return is_changed

    # Перевернуть поле
    def reverse_field(self):
        reversed_field = []

        for x in range(4):
            reversed_field.append([])
            for y in range(4):
                reversed_field[x].append(self.field[x][3 - y])

        self.field = reversed_field.copy()

    # Поменять местами столбцы и строки
    def transpose_field(self):
        transposed_field = []

        for x in range(4):
            transposed_field.append([])
            for y in range(4):
                transposed_field[x].append(self.field[y][x])

        self.field = transposed_field.copy()

    def make_move_left(self):
        is_compressed = self.compress_field()
        is_merged = self.merge_cells()
        is_changed = is_compressed or is_merged

        self.compress_field()

        return is_changed

    def make_move_right(self):
        self.reverse_field()
        is_changed = self.make_move_left()
        self.reverse_field()

        return is_changed

    def make_move_up(self):
        self.transpose_field()
        is_changed = self.make_move_left()
        self.transpose_field()

        return is_changed

    def make_move_down(self):
        self.transpose_field()
        is_changed = self.make_move_right()
        self.transpose_field()

        return is_changed

    def make_move(self, direction):
        if direction == Directions.DOWN:
            return self.make_move_down()
        elif direction == Directions.UP:
            return self.make_move_up()
        elif direction == Directions.LEFT:
            return self.make_move_left()
        elif direction == Directions.RIGHT:
            return self.make_move_right()

    def lose_game(self):
        self.status = Status.LOSED

    def win_game(self):
        self.status = Status.WINNED
