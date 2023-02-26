import pygame

from field import GameField

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


class Graphic_Feld(GameField):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.left = 50
        self.top = 50
        self.cell_size = 80

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, '#bbada0', (
                    (self.left + i * self.cell_size, self.top + j * self.cell_size), (self.cell_size, self.cell_size)),
                                 2)
        print(self.field)


pygame.init()
pygame.display.set_caption('2048')
board = Graphic_Feld(4, 4)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color('#fbf8f1'))
    board.render(screen)
    pygame.display.flip()
