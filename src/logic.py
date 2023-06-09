from __future__ import annotations
from consts import Piece
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .board import Board

from createOffsetMap import QUEEN_OFFSET_MAP, ROOK_OFFSET_MAP, BISHOP_OFFSET_MAP, KNIGHT_MOVE_MAP

board: Board = None
white_move = True
prev_clicked_square = None
legal_moves = [
    (i, j) for i in range(64) for j in range(64)
]


def init_logix(_board):
    global board
    board = _board
    compute_all_legal_moves()

def piece_on(loc):
    """Returns true if a piece exists on the location"""
    return board[loc] != Piece.Empty

def piece_is_white(loc):
    """Returns true if the piece at this location is a white piece"""
    return board[loc] >= Piece.WhitePawn and board[loc] <= Piece.WhiteKing

def target_piece_color_is_correct(loc):
    return piece_on(loc) and \
        (
            (white_move and piece_is_white(loc)) or \
            (not white_move and not piece_is_white(loc))
        )

def king_is_checked_after_move(start, end, king_is_white):
    """
    NOTE: Temporarily makes changes to the board
    """
    king_loc = -1
    for i in range(64):
        if (king_is_white and board[i] == Piece.WhiteKing) or (not king_is_white and board[i] == Piece.BlackKing):
            king_loc = i
            break
    if king_loc == -1:raise Exception("NO KING FOUND ON BOARD!")

    king_is_checked = False

    curr_end = board[end]
    board[end], board[start] = board[start], Piece.Empty

    # Go bishops moves
    # Go rooks moves
    # Go knights moves
    
    # Castling is little bit more wierd

    # revert the changes made
    board[start], board[end] = board[end], curr_end

    return king_is_checked

    

def compute_all_legal_moves():
    """Computes all legal moves possible from the side whos turn it is currently"""
    legal_moves.clear()

    # TODO! Invalidate moves if king is under check after making the move
    for start in range(64):        
        if not target_piece_color_is_correct(start):continue
        if board[start] in (Piece.WhiteBishop, Piece.BlackBishop):
            for offset, max_end in BISHOP_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        legal_moves.append((start, end))
                        continue
                    if not target_piece_color_is_correct(end):
                        legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhiteRook, Piece.BlackRook):
            for offset, max_end in ROOK_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        legal_moves.append((start, end))
                        continue
                    if not target_piece_color_is_correct(end):
                        legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhiteQueen, Piece.BlackQueen):
            for offset, max_end in QUEEN_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        legal_moves.append((start, end))
                        continue
                    if not target_piece_color_is_correct(end):
                        legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhiteKnight, Piece.BlackKnight):
            for end in KNIGHT_MOVE_MAP[start]:
                if not piece_on(end):
                    legal_moves.append((start, end))
                    continue
                if not target_piece_color_is_correct(end):
                    legal_moves.append((start, end))

        elif board[start] in (Piece.WhiteKing, Piece.BlackKing):
            # TODO!
            # Need to check for castling
            for offset, max_end in QUEEN_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        legal_moves.append((start, end))
                        break # We can only move like one square at a time
                    if not target_piece_color_is_correct(end):
                        legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhitePawn, Piece.BlackPawn):
            # TODO! Need to handle promotion
            # TODO! Need to check for empassant
            direction = -8 if white_move else +8
            if not piece_on(start + direction):
                legal_moves.append((start, start + direction))
                
            if ((white_move and start//8 == 6) or (not white_move and start//8 == 1)) and not piece_on(start + direction*2):
                legal_moves.append((start, start + direction*2))

            if (start%8 != 7) and piece_on(start + direction + 1) and not target_piece_color_is_correct(start + direction + 1):
                legal_moves.append((start, start + direction + 1))

            if (start%8 != 0) and piece_on(start + direction - 1) and not target_piece_color_is_correct(start + direction - 1):
                legal_moves.append((start, start + direction - 1))

def handle_click(loc):
    global prev_clicked_square, white_move

    if prev_clicked_square is not None and target_piece_color_is_correct(prev_clicked_square):
        if loc == prev_clicked_square:return False
        if (prev_clicked_square, loc) not in legal_moves:
            prev_clicked_square = None
            return False

        board[prev_clicked_square], board[loc] = 0, board[prev_clicked_square]
        white_move = not white_move
        prev_clicked_square = None
        compute_all_legal_moves()
        return True
    else:
        prev_clicked_square = loc
        return False
    
