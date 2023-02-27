import pygame
from field import Directions
from field import Status
from field import GameField

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


class GraphicsField(GameField):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.left = 50
        self.top = 50
        self.cell_size = 80
        self.field = GameField()
        self.field.add_piece()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_score(self):
        return self.field.get_score()

    def load_field(self, new_field):
        self.field = new_field

    def get_field(self):
        return self.field

    def set_text(self, screen, value, cords):
        font_color = pygame.Color('#696153')
        font = pygame.font.Font(None, 50)
        text = font.render(str(value), True, font_color)
        width_text = text.get_width() // 2
        height_text = text.get_height() // 2
        cords = cords[0] - width_text, cords[1] - height_text
        screen.blit(text, cords)

    def render(self, screen):
        # For each color there are unique color
        color_values = {
            2: '#eae0d4',
            4: '#e9dfc3',
            8: '#eead77',
            16: '#ea9260',
            32: '#f2765b',
            64: '#f25836',
            128: '#e6cc6c',
            256: '#f1d14a',
            512: '#efc451',
            1024: '#ecc43f',
            2048: '#eec22e',
        }
        for i in range(self.width):
            for j in range(self.height):
                cell_value = self.field.field[j][i]
                cords = [self.left + i * self.cell_size, self.top + j * self.cell_size]
                w, h = (self.cell_size, self.cell_size)
                if cell_value:
                    cell_color = color_values[cell_value]
                else:
                    cell_color = '#cdc1b5'
                pygame.draw.rect(screen, cell_color, (cords, (w, h)))
                pygame.draw.rect(screen, '#bbada0', (cords, (w + 4, h + 4)), 4)
                if cell_value:
                    x1, y1 = cords[0] + self.cell_size // 2, cords[1] + self.cell_size // 2
                    self.set_text(screen, cell_value, (x1, y1))


pygame.init()
pygame.display.set_caption('2048')
board = GraphicsField(4, 4)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

try:
    board.get_field().load_game()
except Exception as e:
    print("Unable to load game due to " + str(e))

running = True
while running:
    if board.get_field().status == Status.LOSED:
        # TODO: losing message
        new_field = GameField()
        board.load_field(new_field)
    elif board.get_field().status == Status.WINNED:
        # TODO: winning message
        new_field = GameField()
        board.load_field(new_field)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            direction = None
            key = event.key
            if key == pygame.K_UP or key == pygame.K_w:
                direction = Directions.UP
            if key == pygame.K_DOWN or key == pygame.K_s:
                direction = Directions.DOWN
            if key == pygame.K_LEFT or key == pygame.K_a:
                direction = Directions.LEFT
            if key == pygame.K_RIGHT or key == pygame.K_d:
                direction = Directions.RIGHT
            if direction is None:
                pass  # TODO: you cannot move like that message
            else:
                is_changed = board.get_field().make_move(direction)
                if not is_changed:
                    # TODO: you cannot move like that message
                    pass
                else:
                    board.get_field().add_piece()
                    try:
                        board.get_field().save_game()
                    except Exception as e:
                        print("Unable to save game due to " + str(e))
                # FIXME: delete it
                for x in range(4):
                    for y in range(4):
                        if board.get_field().field[x][y] is None:
                            print("0\t", end="")
                            continue
                        print(str(board.get_field().field[x][y]) + "\t", end="")
                    print()
                print("---")
                # FIXME: end
    screen.fill(pygame.Color('#fbf8f1'))
    board.render(screen)
    pygame.display.flip()