import sys
import pygame
from pygame.locals import QUIT
from board import draw_board

pygame.init()


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BG_COLOR = (100, 100, 100)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello world")

def main():
    while True:
        SCREEN.fill(BG_COLOR)
        draw_board(SCREEN, SCREEN_WIDTH)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
