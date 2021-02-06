import sys
import pygame

class Board: 

    def __init__(self, square_size, pos):
        self.pos = pos # Coordinate of top-left corner of the board 
        self.square_size = square_size
        self.board =[
            [None for i in range(5)] for x in range(5)
        ] 
        self.check = False
        self.chekmate = False

    #Adds pieces to the board
    def initialize(self):
        pass

    def draw(self, screen):
        square_size = self.square_size
        square_x = self.pos[0]
        square_y = self.pos[1] - square_size 
        BLACK = (0 , 0, 0)
        WHITE = (255 , 255, 255)
        square_color = BLACK
        for row in range(5):
            square_x = self.pos[0]
            square_y = square_y + square_size 
            for col in range(5):
                    square_x = square_x + square_size
                    pygame.draw.rect(
                        screen, square_color, 
                        (square_x, square_y, square_size, square_size)
                    )
                    square_color = \
                        BLACK if square_color == WHITE else WHITE
