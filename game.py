import sys
import pygame
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN
)
from piece import (
    Piece,
    PieceType,
)
from board import (
    Board, get_square_from_point,
    get_square_center, get_legal_moves
)



#TODOS:
'''
1 - Make a board ***
2 - Add pieces to the board ***
3 - Allow player input  ***
4 - Disallow invalid moves **
5 - Show valid moves on the board **
6 - Allow piece captures **
7 - Checks for potential checks before moves **
- Implement turn changes
- Implement promotion ??
- Implement Casteling ??
? - Implement minimax
'''


pygame.init()


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BG_COLOR = (0, 0, 0)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess minimax")

def draw_user_guides(board, selected_piece, available_moves):
    #Draw circle guides that will help the user move and know
    #which piece is selected
    CIRCLE_COLOR = (50, 155, 168)
    pygame.draw.circle(
        SCREEN,
        CIRCLE_COLOR,
        get_square_center(board, *selected_piece),
        40,
        width = 4
    )

    for move in available_moves:
        pygame.draw.circle(
            SCREEN,
            CIRCLE_COLOR,
            get_square_center(board, *move),
            3,
        )

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
            if not selected_piece:
                if not board.is_square_free(pos):
                    selected_piece = pos
            else:
                player_moved = True


        if selected_piece:
            available_moves = get_legal_moves(board, selected_piece)
            #Check if a move puts king in check.
            #If it does, it isn't a legal move
            piece = board.get_piece(selected_piece)
            color = piece.color
            bad_moves = []
            for move in available_moves:
                x, y = selected_piece
                x1, y1 = move
                aux = board.get_piece(move)
                board.board[y1][x1] = board.board[y][x]
                board.board[y][x] = None
                if board.color_in_check(color):
                    bad_moves.append(move)
                #Revert board
                board.board[y1][x1] = aux
                board.board[y][x] = piece
            for move in bad_moves:
                available_moves.remove(move)
            draw_user_guides(board, selected_piece, available_moves)

        #Process a player move
        if player_moved:
            if pos in available_moves:
                board.move_piece(selected_piece, pos)
            player_moved = False
            selected_piece = None

        pos = None
        pygame.display.update()

if __name__ == "__main__":
    main()
