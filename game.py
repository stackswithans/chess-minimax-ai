import sys
import pygame
from pygame.locals import QUIT
from board import Board



#TODOS:
'''
1 - Make a board ***
2 - Add pieces to the board
3 - Allow player input  
4 - Show valid moves on the board
5 - Disallow invalid moves
6 - Implement minimax
'''


pygame.init()


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BG_COLOR = (0, 0, 0)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello world")

def main():
    square_size = 80
    board = Board(
        square_size,
        (
            (SCREEN_WIDTH - (square_size * 5)) / 2, 
            (SCREEN_HEIGHT - (square_size * 5)) / 2,
        ) 
    ) 
    while True:
        SCREEN.fill(BG_COLOR)

        board.draw(SCREEN)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
