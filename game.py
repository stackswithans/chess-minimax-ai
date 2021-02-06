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
    pos = None
    selected_piece = None
    player_moved = False
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


        #Process click event
        if pos is not None:
            board_piece = board.board[pos[0]][pos[1]]
            if board_piece:
                selected_piece = pos
            else:
                if selected_piece:
                    player_moved = True
                else: 
                    selected_piece = None
        else:
            selected_piece = None

        #Draw circle if a piece was selected
        if selected_piece is not None:
            pygame.draw.circle(
                SCREEN,
                (0, 0, 0),
                get_square_center(board, *selected_piece),
                40,
                width = 4
            )

        #Process a player move
        if player_moved:
            board.board[pos[0]][pos[1]] = \
                board.board[selected_piece[0]][selected_piece[1]]
            board.board[selected_piece[0]][selected_piece[1]] = None
            player_moved = False
            selected_piece = None
            pos = None



        pygame.display.update()

if __name__ == "__main__":
    main()
