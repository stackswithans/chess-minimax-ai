import sys
import pygame
import piece

#Converts board coordinates like (0,0) to screen coordinates of
#The corresponding square (top-left)
def convert_coordinates(board, row, col):
    return (
        board.pos[0] + (board.square_size * col), 
        board.pos[1] + (board.square_size * row)
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
        self.board[1][1] = piece.B_KING

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

        piece_size = 60
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece is not None:
                    pos_x, pos_y = convert_coordinates(self, r, c)
                    screen.blit(
                        piece, 
                        (pos_x , pos_y)
                    ) 

