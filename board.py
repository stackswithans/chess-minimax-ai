import sys
import pygame

def draw_board(screen, screen_width, board=None):
    square_size = 100
    square_x = ((screen_width - (square_size * 5)) / 2)
    square_y = -square_size 
    BLACK = (0 , 0, 0)
    WHITE = (255 , 255, 255)
    square_color = BLACK
    for row in range(5):
        square_x = ((screen_width - (square_size * 5)) / 2)
        square_y = square_y + square_size 
        for col in range(5):
                square_x = square_x + square_size
                pygame.draw.rect(
                    screen, square_color, 
                    (square_x, square_y, square_size, square_size)
                )
                square_color = \
                    BLACK if square_color == WHITE else WHITE
