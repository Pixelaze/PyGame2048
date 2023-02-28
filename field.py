from random import randint
import csv

SAVE_FILE_NAME = "data.csv"
BEST_SCORE_FILE_NAME = ".best_score"
CURRENT_SCORE_FILE_NAME = ".current_score"

BEST_SCORE = 0


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
        self.score = 0

    def get_best_score(self):
        global BEST_SCORE
        return BEST_SCORE

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
        chance = randint(0, 100)
        if chance <= 66:
            self.field[x][y] = 2
        else:
            self.field[x][y] = 4

    def get_status(self):
        self.check_state()
        return self.status

    def check_state(self):
        for i in range(4):
            for j in range(4):
                if self.field[i][j] is None:
                    continue
                if self.field[i][j] >= 2048:
                    self.win_game()

        for x in range(4):
            for y in range(4):
                if self.field[x][y] is None:
                    return

        for x in range(3):
            if self.field[x][3] == self.field[x + 1][3]:
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
                    self.score += self.field[x][y]
                    self.update_best_score()
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
        self.check_state()

        if direction == Directions.DOWN:
            result = self.make_move_down()
        elif direction == Directions.UP:
            result = self.make_move_up()
        elif direction == Directions.LEFT:
            result = self.make_move_left()
        elif direction == Directions.RIGHT:
            result = self.make_move_right()
        
        self.check_state()

        return result

    def update_best_score(self):
        global BEST_SCORE
        if self.score > BEST_SCORE:
            print(BEST_SCORE)
            BEST_SCORE = self.score
            with open(BEST_SCORE_FILE_NAME, "w", encoding="utf-8") as save_file:
                save_file.write(str(BEST_SCORE))

    def lose_game(self):
        self.update_best_score()
        self.status = Status.LOSED

    def win_game(self):
        self.update_best_score()
        self.status = Status.WINNED

    def get_score(self):
        return self.score

    def load_game(self):
        global BEST_SCORE
        with open(BEST_SCORE_FILE_NAME, "r", encoding="utf-8") as load_file:
            BEST_SCORE = int(load_file.read().strip("\n"))

        with open(CURRENT_SCORE_FILE_NAME, "r", encoding="utf-8") as load_file:
            self.score = int(load_file.read().strip("\n"))

        with open(SAVE_FILE_NAME, encoding="utf-8") as load_file:
            for i in range(4):
                self.field[i] = [int(elem) for elem in load_file.readline().strip("\n").split(";")]
                for j in range(4):
                    if self.field[i][j] == 0:
                        self.field[i][j] = None

    def save_game(self):
        with open(BEST_SCORE_FILE_NAME, "w", encoding="utf-8") as save_file:
            save_file.write(str(BEST_SCORE))

        with open(CURRENT_SCORE_FILE_NAME, "w", encoding="utf-8") as save_file:
            save_file.write(str(self.score))

        with open(SAVE_FILE_NAME, "w", encoding="utf-8") as save_file:
            for i in range(4):
                for j in range(3):
                    if self.field[i][j] is None:
                        save_file.write("0;")
                    else:
                        save_file.write(str(self.field[i][j]) + ";")
                if self.field[i][3] is None:
                    save_file.write("0\n")
                else:
                    save_file.write(str(self.field[i][3]) + "\n")
