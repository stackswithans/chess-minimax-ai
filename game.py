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
    get_square_center, get_legal_moves,
    filter_legal_moves
)

from minimax import minimax



#TODOS:
'''
1 - Make a board ***
2 - Add pieces to the board ***
3 - Allow player input  ***
4 - Disallow invalid moves **
5 - Show valid moves on the board **
6 - Allow piece captures **
7 - Checks for potential checks before moves **
- Implement turn changes **
- Implement Checkmate **
- Implement Stalemate **
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


def show_end_screen(text, pos):
    screen = SCREEN.convert_alpha()
    pygame.draw.rect(
        screen, (255, 255, 255, 100 ), 
        (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    fontObj = pygame.font.Font('./res/roboto_slab.ttf', 32)
    textSurfaceObj = fontObj.render(
        text, True, (0, 0, 0)
    )
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = pos
    screen.blit(textSurfaceObj, textRectObj)
    SCREEN.blit(screen, (0, 0))

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

    #Player that's going to move next
    next_move = Piece.WHITE  

    #Postition of mouse clicks
    pos = None
    #Board position of selected piece
    selected_piece = None
    #Player moved piece
    player_moved = False
    while True:
        SCREEN.fill(BG_COLOR)
        board.draw(SCREEN)

        #Check if player is mated
        if board.checkmate.get(next_move):
            winner = Piece.BLACK if next_move == Piece.WHITE\
                else Piece.WHITE
            show_end_screen(f"{winner.capitalize()} has won.", 
               ( SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 
            )
        elif board.has_no_moves(next_move):
        #Check if game ends in stalemate
            show_end_screen(
                f"No valid moves. Game ends in stalemate.", 
               ( SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 
            )

        #AI's turn
        if next_move == Piece.BLACK:
            pos, move = minimax(
                board, maximizing=True, 
                depth=0, max_depth=3 
            )
            board.move_piece(pos, move)
            next_move = Piece.WHITE
            continue
            
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
                    piece = board.get_piece(pos)
                    if piece.color == next_move: 
                        selected_piece = pos
            else:
                player_moved = True


        if selected_piece:
            available_moves = get_legal_moves(board, selected_piece)
            available_moves = filter_legal_moves(
                board, selected_piece, available_moves
            )
            draw_user_guides(board, selected_piece, available_moves)

        #Process a player move
        if player_moved:
            if pos in available_moves:
                board.move_piece(selected_piece, pos)
                # Change turn
                next_move = Piece.BLACK if next_move == Piece.WHITE\
                    else Piece.WHITE
            player_moved = False
            selected_piece = None

        pos = None
        pygame.display.update()

if __name__ == "__main__":
    main()
