import sys
import pygame
import time
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
- Implement minimax **
- Use a better cutoff test
- Implement alpha_beta pruning 
- Implement promotion ??
- Implement Casteling ??
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
def convert_to_chess_notation(old_pos, new_pos):
    rows = {
        0 : 5,
        1 : 4,
        2 : 3,
        3 : 2,
        4 : 1,
    }
    ranks = {}
    for i, c in enumerate("abcde"):
        ranks[i] = c

    origin = ranks[old_pos[0]] + str(rows[old_pos[1]])
    dest = ranks[new_pos[0]] + str(rows[new_pos[1]])
    return f"{origin}{dest}"

def save_game(board):
    #Write moves to files
    with open("black.txt", "w") as black_log, \
         open("white.txt", "w") as white_log:
        black_log.write("Start game\n")
        white_log.write("Start game\n")
        white_log.write("White\n")
        black_log.write("Black\n")
        for move in board.moves:
            chess_not = convert_to_chess_notation(*move[1]) 
            if move[0] == Piece.BLACK:
                black_log.write(f"{chess_not}\n")
                white_log.write(f"Black played {chess_not}\n")
            else:
                white_log.write(f"{chess_not}\n")
                black_log.write(f"White played {chess_not}\n")

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

            t1 = time.time()
            choice = minimax(
                board, maximizing=True, 
                depth=0, max_depth=4
            )
            current_pos, move = choice
            board.move_piece(current_pos, move)
            next_move = Piece.WHITE
            continue
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                save_game(board)
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
