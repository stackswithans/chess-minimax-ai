import sys
import pygame
from pygame.locals import QUIT

pygame.init()


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BG_COLOR = (100, 100, 100)


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello world")

def draw_board():
    square_size = 100
    square_x = (SCREEN_WIDTH / 2) - (square_size * 5)
    square_y = 0 
    BLACK = (0 , 0, 0)
    WHITE = (255 , 255, 255)
    square_color = BLACK
    for row in range(5):
        square_x = (SCREEN_WIDTH / 2) - (square_size * 5)
        if row > 0:
            square_y = square_y + square_size 
        for col in range(5):
                square_x = square_x + square_size
                pygame.draw.rect(
                    SCREEN, square_color, 
                    (square_x, square_y, square_size, square_size)
                )
                square_color = BLACK if square_color == WHITE else WHITE


def main():
    while True:
        SCREEN.fill(BG_COLOR)
        draw_board()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()




if __name__ == "__main__":
    main()
