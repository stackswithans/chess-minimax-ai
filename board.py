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
def get_point_from_square(board, row, col):
    return (
        board.pos[0] + (board.square_size * col), 
        board.pos[1] + (board.square_size * row)
    )

#Gets the coordinate of a square on the board based on a point in
#the screen
def get_square_from_point(board, x, y):
    square_size = board.square_size
    board_size = square_size * 5
    for r in range(board_size):
        for c in range(board_size):
            grid_x, grid_y = get_point_from_square(board, r, c)
            square = pygame.Rect(
                grid_x, grid_y, square_size, square_size
            )
            if square.collidepoint(x, y):
                return (r, c)
    return None

def get_square_center(board, row, col):
    x, y = get_point_from_square(board, row, col)
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
        self.check = False
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
                    Piece.WHITE if r == 1 else Piece.BLACK
                )
                self.board[r][c] = piece_obj
                continue
            piece, image, color = pieces[next_piece]
            piece_obj = Piece(piece, image, color)
            self.board[r][c] = piece_obj
            next_piece += 1

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

        #Draw pieces
        piece_size = 60
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece is not None:
                    pos_x, pos_y = get_square_center(self, r, c)
                    screen.blit(
                        piece.image, 
                        (
                            pos_x - piece_size / 2 , 
                            pos_y - piece_size / 2,
                        )
                    ) 

