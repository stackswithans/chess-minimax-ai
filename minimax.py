from board import get_legal_moves, filter_legal_moves
from piece import Piece, PieceType
import math


def calculate_material(board, pieces):
    material = 0
    points = {
        PieceType.QUEEN: 9, 
        PieceType.ROOK: 5, 
        PieceType.KNIGHT: 3, 
        PieceType.BISHOP: 3, 
        PieceType.PAWN: 1, 
        PieceType.KING: 0, 
    }
    for piece in pieces:
        piece_obj = board.get_piece(piece)
        if not piece_obj:
            continue
        material += points[piece_obj.ptype]
    return material


def minimax_value(board, maximizing, depth, max_depth=3):
    color = Piece.BLACK if maximizing else Piece.WHITE

    pieces = board.get_pieces_by_color(color)
    in_check = board.color_in_check(color)
    no_moves = board.has_no_moves(color)
    #Check if games is over
    if in_check and no_moves:
        return float("-inf") if maximizing else float("inf")
    elif no_moves:
        return 0
    elif depth == max_depth:
        #If max depth has been reached, calculate board material
        opp_color = Piece.WHITE if color == Piece.BLACK\
            else Piece.BLACK
        opp_pieces = board.get_pieces_by_color(opp_color)
        material = calculate_material(board, pieces)
        opp_material = calculate_material(board, opp_pieces) 
        # Do some mathss
        if maximizing:
            return material - opp_material
        else:
            return opp_material - material
    values = []
    for piece in pieces:
        moves = get_legal_moves(board, piece)
        moves = filter_legal_moves(board, piece, moves)
        for move in moves:
            piece_obj = board.get_piece(piece)
            x, y = piece
            x1, y1 = move
            aux = board.get_piece(move)
            board.board[y1][x1] = board.board[y][x]
            board.board[y][x] = None
            value = minimax_value(
                board, not maximizing, depth + 1, max_depth
            )
            values.append(value)
            #Revert board
            board.board[y1][x1] = aux
            board.board[y][x] = piece_obj
    #Return value
    func = max if maximizing else min
    return func(values)



#Calculates the optimal move for the 'bot'
#using minimax
def minimax(board):
    #Get all available moves
    color = Piece.BLACK
    pieces = board.get_pieces_by_color(color)
    values = []
    for piece in pieces:
        moves = get_legal_moves(board, piece)
        moves = filter_legal_moves(board, piece, moves)
        for move in moves:
            piece_obj = board.get_piece(piece)
            x, y = piece
            x1, y1 = move
            aux = board.get_piece(move)
            board.board[y1][x1] = board.board[y][x]
            board.board[y][x] = None
            value = minimax_value(board, False, 1) #Not my turn
            #Revert board
            board.board[y1][x1] = aux
            board.board[y][x] = piece_obj
            values.append((value, (piece, move)))

    result = max(values, key=lambda move: move[0])
    print("Chosen move:", result[1], "Heuristic value:", result[0])
    return result[1]
