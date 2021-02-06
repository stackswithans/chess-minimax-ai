import os.path as path
from enum import Enum
import pygame


RES_DIR = path.abspath("./res")

#Load black pieces
B_KING = pygame.image.load(path.join(RES_DIR, "black_king.png"))
B_QUEEN = pygame.image.load(path.join(RES_DIR, "black_queen.png"))
B_ROOK = pygame.image.load(path.join(RES_DIR, "black_rook.png"))
B_BISHOP = pygame.image.load(path.join(RES_DIR, "black_bishop.png"))
B_KNIGHT = pygame.image.load(path.join(RES_DIR, "black_knight.png"))
B_PAWN = (pygame.image.load, path.join(RES_DIR, "black_pawn.png"))

#Load white pieces
W_KING = pygame.image.load(path.join(RES_DIR, "white_king.png"))
W_QUEEN = pygame.image.load(path.join(RES_DIR, "white_queen.png"))
W_ROOK = pygame.image.load(path.join(RES_DIR, "white_rook.png"))
W_BISHOP = pygame.image.load(path.join(RES_DIR, "white_bishop.png"))
W_KNIGHT = pygame.image.load(path.join(RES_DIR, "white_knight.png"))
W_PAWN = (pygame.image.load, path.join(RES_DIR, "white_pawn.png"))

class PieceType(Enum):
    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN = "pawn"

class Piece:
    WHITE = "white"
    BLACK = "black"

    def __init__(self, ptype, image, color):
        self.ptype = ptype
        self.image = image
        self.color = color

