import sys
import pygame
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN
)
from board import (
    Board, get_square_from_point,
    get_square_center
)



#TODOS:
'''
1 - Make a board ***
2 - Add pieces to the board ***
3 - Allow player input  
4 - Disallow invalid moves
5 - Show valid moves on the board
6 - Implement minimax
'''


pygame.init()


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BG_COLOR = (0, 0, 0)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess minimax")

def main():
    square_size = 80
    board = Board(
        square_size,
        (
            (SCREEN_WIDTH - (square_size * 5)) / 2, 
            (SCREEN_HEIGHT - (square_size * 5)) / 2,
        ) 
    ) 
    selected_piece = None
    while True:
        SCREEN.fill(BG_COLOR)
        board.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos = get_square_from_point(
                    board, *event.pos
                )
                if pos is not None:
                    if board.board[pos[0]][pos[1]] is not None:
                        selected_piece = pos
                    continue
                selected_piece = None

        if selected_piece is not None:
            pygame.draw.circle(
                SCREEN,
                (0, 0, 0),
                get_square_center(board, *selected_piece),
                40,
                width = 4
            )

        pygame.display.update()

if __name__ == "__main__":
    main()
