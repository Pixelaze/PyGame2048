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

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, '#bbada0', (
                    (self.left + i * self.cell_size, self.top + j * self.cell_size), (self.cell_size, self.cell_size)),
                                 2)
                #print(self.field.field[i][j])  # EXAMPLE: this returns the cell value
                                                # None should be 0


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
                pass # TODO: you cannot move like that message
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
