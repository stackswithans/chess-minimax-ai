import sys
import pygame
import itertools
from piece import (
    B_KING,
    B_QUEEN,
    B_ROOK,
    B_BISHOP,
    B_KNIGHT, 
    B_PAWN,
    W_KING,
    W_QUEEN,
    W_ROOK,
    W_BISHOP,
    W_KNIGHT, 
    W_PAWN,
    PieceType,
    Piece
)

#Converts board coordinates like (0,0) to screen coordinates of
#The corresponding square (top-left)
def get_point_from_square(board, col, row):
    return (
        board.pos[0] + (board.square_size * col), 
        board.pos[1] + (board.square_size * row)
    )

#Gets the coordinate of a square on the board based on a point in
#the screen
def get_square_from_point(board, x, y):
    square_size = board.square_size
    board_size = 5
    for r in range(board_size):
        for c in range(board_size):
            grid_x, grid_y = get_point_from_square(board, c, r)
            square = pygame.Rect(
                grid_x, grid_y, square_size, square_size
            )
            if square.collidepoint(x, y):
                return (c, r)
    return None

def get_square_center(board, col, row):
    x, y = get_point_from_square(board, col, row)
    return (
        (x + board.square_size / 2), 
        (y + board.square_size / 2)  
    )


class Board: 
    def __init__(self, square_size, pos):
        self.pos = pos # Coordinate of top-left corner of the board 
        self.square_size = square_size
        self.board =[
            [None for i in range(5)] for x in range(5)
        ] 
        self.white_in_check = False
        self.black_in_check = False
        self.chekmate = False
        self.initialize()

    #Adds pieces to the board
    def initialize(self):
        pieces = [
            #Black pieces
            (PieceType.ROOK, B_ROOK, Piece.BLACK),
            (PieceType.KNIGHT, B_KNIGHT, Piece.BLACK),
            (PieceType.BISHOP, B_BISHOP, Piece.BLACK),
            (PieceType.QUEEN, B_QUEEN, Piece.BLACK),
            (PieceType.KING, B_KING, Piece.BLACK),
            #White pieces
            (PieceType.ROOK, W_ROOK, Piece.WHITE),
            (PieceType.KNIGHT, W_KNIGHT, Piece.WHITE),
            (PieceType.BISHOP, W_BISHOP, Piece.WHITE),
            (PieceType.QUEEN, W_QUEEN, Piece.WHITE),
            (PieceType.KING, W_KING, Piece.WHITE),

        ]
        #Add pieces
        next_piece = 0
        #This was done just to make the code look prettier
        for r, c  in itertools.product(range(5), range(5)):
            if r == 2:
                continue
            # Adds pawn rows
            if r == 1 or r ==3:
                loader, filepath = B_PAWN if r == 1 else W_PAWN
                piece_obj = Piece(
                    PieceType.PAWN, 
                    loader(filepath),
                    Piece.BLACK if r == 1 else Piece.WHITE
                )
                self.board[r][c] = piece_obj
                continue
            piece, image, color = pieces[next_piece]
            piece_obj = Piece(piece, image, color)
            self.board[r][c] = piece_obj
            next_piece += 1

    def get_pos_by_ptype(self, ptype, color):
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece and piece.ptype == ptype and piece.color == color:
                    return (c, r)
        return None

    def color_in_check(self, color):
        king_pos = self.get_pos_by_ptype(PieceType.KING, color)

        attackers = [] 
        for r, row in enumerate(self.board):
            for c, other_piece in enumerate(row):
                pos = (c, r)
                if other_piece and \
                other_piece.color != color and \
                king_pos in get_legal_moves(self, pos):
                    attackers.append(pos)
        if len(attackers):
            return True
        return False


    def move_piece(self, old_pos, new_pos):
        x, y = old_pos
        x1, y1 = new_pos
        self.board[y1][x1] = self.board[y][x]
        self.board[y][x] = None
        #Check if move triggers check
        piece = self.get_piece(new_pos)
        color = Piece.BLACK if piece.color == Piece.WHITE \
            else Piece.WHITE
        self.black_in_check = self.color_in_check(Piece.BLACK)
        self.white_in_check = self.color_in_check(Piece.WHITE)


    def get_piece(self, square):
        x, y = square
        #HACK: returns false on out of bounds move
        if (x > 4 or x < 0) or (y < 0 or y > 4):
            return None
        return self.board[y][x]

    def is_square_free(self, square):
        x, y = square
        #HACK: returns false on out of bounds move
        if (x > 4 or x < 0) or (y < 0 or y > 4):
            return False
        return self.board[y][x] is None

    def draw(self, screen):
        square_size = self.square_size
        square_x = self.pos[0]
        square_y = self.pos[1]
        BLACK = (50 , 50, 50)
        WHITE = (255 , 255, 255)
        square_color = BLACK
        for row in range(5):
            for col in range(5):
                    pygame.draw.rect(
                        screen, square_color, 
                        (square_x, square_y, square_size, square_size)
                    )
                    square_color = \
                        BLACK if square_color == WHITE else WHITE
                    square_x = square_x + square_size
            square_y = square_y + square_size 
            square_x = self.pos[0]
        center = get_square_center(self, 0 , 0)

        #Paint king square red if in check
        if self.white_in_check or self.black_in_check:
            square_color = (212, 40, 21)
            color = Piece.WHITE if self.white_in_check\
                else Piece.BLACK
            king_pos = self.get_pos_by_ptype(PieceType.KING, color)
            x, y = get_point_from_square(self, *king_pos)
            pygame.draw.rect(
                screen, square_color, 
                (x, y, square_size, square_size)
            )

        #Draw pieces
        piece_size = 60
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece is not None:
                    pos_x, pos_y = get_square_center(self, c, r)
                    screen.blit(
                        piece.image, 
                        (
                            pos_x - piece_size / 2 , 
                            pos_y - piece_size / 2,
                        )
                    ) 


def move_is_capture(piece, other_piece):
    if other_piece and other_piece.color != piece.color:
        return True
    return False

# Gets all horizontal and vertical moves for a piece
# i.e rook or queen
def get_hv_moves(board, square):
    moves = []
    piece = board.get_piece(square)
    #Get all vertical moves
    row = square[1]
    up_down = (row + 1, row - 1)
    for r in up_down:
        while board.is_square_free((square[0], r)):
            moves.append((square[0], r))
            r = r - 1 if r < row else r + 1
        other_piece = board.get_piece((square[0], r))
        if move_is_capture(piece, other_piece):
            moves.append((square[0], r))
    #Get all horizontal moves
    col = square[0]
    left_right = (col + 1, col - 1)
    for c in left_right:
        while board.is_square_free((c, square[1])):
            moves.append((c, square[1]))
            c = c - 1 if c < col else c + 1
        other_piece = board.get_piece((c, square[1]))
        if move_is_capture(piece, other_piece):
            moves.append((c, square[1]))

    return moves

def get_diag_moves(board, square):
    moves = []
    piece = board.get_piece(square)
    #Get front diagonals
    col = square[0]
    row = square[1]
    diag_1 = ((col - 1, row + 1), (col + 1, row + 1))
    for diag in diag_1:
        x, y = diag
        while board.is_square_free((x, y)):
            moves.append((x, y))
            y += 1
            x = x - 1 if x < col else x + 1
        other_piece = board.get_piece((x, y))
        if move_is_capture(piece, other_piece):
            moves.append((x, y))
    #Get all horizontal moves
    diag_2 = ((col - 1, row - 1), (col + 1, row - 1))
    for diag in diag_2:
        x, y = diag
        while board.is_square_free((x, y)):
            moves.append((x, y))
            y -= 1
            x = x - 1 if x < col else x + 1
        other_piece = board.get_piece((x, y))
        if move_is_capture(piece, other_piece):
            moves.append((x, y))

    return moves



def get_legal_moves(board, square):
    moves = []
    #Get all valid moves for the selected piece
    pos_x, pos_y = square
    piece = board.get_piece(square)

    ptype = piece.ptype
    if ptype == PieceType.PAWN:
        is_black = piece.color == Piece.BLACK
        straight_move = (pos_x, pos_y + 1) if is_black \
            else (pos_x, pos_y - 1)
        #Check for move by one square
        if board.is_square_free(straight_move):
            moves.append(straight_move)
        # Check for diagonal moves
        #First diag
        diag_move_1 = (pos_x + 1, pos_y + 1) if is_black \
            else (pos_x - 1, pos_y - 1)
        #Second diag
        diag_move_2 = (pos_x - 1, pos_y + 1) if is_black \
            else (pos_x + 1, pos_y - 1)
        for move in (diag_move_1, diag_move_2):
            other_piece = board.get_piece(move)
            if move_is_capture(piece, other_piece):
                moves.append(move)

    elif ptype == PieceType.KING:
        col, row = square
        king_moves = (
            (col, row + 1),
            (col, row - 1),
            (col - 1, row),
            (col + 1, row),
            (col - 1, row - 1),
            (col + 1, row - 1),
            (col - 1, row + 1),
            (col + 1, row + 1),
        )

        for king_move in king_moves:
            square_free = board.is_square_free(king_move)
            other_piece = board.get_piece(king_move)
            if square_free or move_is_capture(piece, other_piece):
                moves.append(king_move)

    elif ptype == PieceType.ROOK:
        moves = get_hv_moves(board, square)

    elif ptype == PieceType.BISHOP:
        moves = get_diag_moves(board, square)

    elif ptype == PieceType.QUEEN:
        moves = get_hv_moves(board, square) + \
                get_diag_moves(board, square)

    elif ptype == PieceType.KNIGHT:
        col, row  = square
        orth_moves = (
            (col + 1, row + 2),
            (col - 1, row + 2),
            (col - 1, row - 2),
            (col + 1, row - 2),
            (col - 2, row + 1),
            (col + 2, row + 1),
            (col - 2, row - 1),
            (col + 2, row - 1),
        )
        for orth_move in orth_moves:
            square_free = board.is_square_free(orth_move)
            other_piece = board.get_piece(orth_move)
            if square_free or move_is_capture(piece, other_piece):
                moves.append(orth_move)


    return moves
