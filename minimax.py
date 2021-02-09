from board import (
    get_legal_moves, filter_legal_moves,
    move_is_capture
)
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

#Sorts moves to improve the performance
#of alpha beta prunnning
def sort_moves(board, piece, moves):
    priority = []
    unimportant = []
    for move in moves:
        piece_obj = board.get_piece(piece)
        other_piece = board.get_piece(move)
        if move_is_capture(piece_obj, other_piece):
            priority.append(move)
            continue
        unimportant.append(move)
    return priority + unimportant



#Calculates the optimal move for the 'bot'
#using minimax
def minimax(
        board, maximizing=True, alpha=float("-inf"), 
        beta=float("inf"), depth=0, max_depth=4
    ):
    color = Piece.BLACK if maximizing else Piece.WHITE

    pieces = board.get_pieces_by_color(color)
    in_check = board.color_in_check(color)
    no_moves = board.has_no_moves(color)
    #Check if games is over
    if in_check and no_moves:
        return float("-inf") if maximizing else float("inf")
    elif no_moves:
        return 0
    if depth == max_depth:
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
    #Calcular heurística para os estados filhos
    operators = []
    for piece in pieces:
        moves = get_legal_moves(board, piece)
        moves = filter_legal_moves(board, piece, moves)
        moves = sort_moves(board, piece, moves)
        for move in moves:
            piece_obj = board.get_piece(piece)
            operators.append((piece, move))

    max_min_value = float("-inf") if maximizing else float("inf")
    cmp_func = max if maximizing else min
    chosen_op = None
    for operator in operators:
        piece, move = operator
        x, y = piece
        x1, y1 = move
        piece_obj = board.get_piece(piece)
        aux = board.get_piece(move)
        board.board[y1][x1] = board.board[y][x]
        board.board[y][x] = None
        value = minimax(
            board, not maximizing,
            alpha, beta, 
            depth + 1, max_depth
        ) #Not my turn
        #Revert board
        max_min_value = cmp_func([max_min_value, value])
        board.board[y1][x1] = aux
        board.board[y][x] = piece_obj
        if depth == 0:
            if max_min_value == value:
                chosen_op = (value, (piece, move))
        else:
            if maximizing:
                alpha = max([alpha, value])
                if alpha >= beta: 
                    break
            else:
                beta = min([beta, value])
                if beta <= alpha:
                    break

    #Return a move if we are at the root of the search tree
    if depth == 0:
        return chosen_op[1]
    return max_min_value
