from __future__ import annotations
from consts import Piece, Theatrics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .board import Board

from createOffsetMap import QUEEN_OFFSET_MAP, ROOK_OFFSET_MAP, BISHOP_OFFSET_MAP, KNIGHT_MOVE_MAP

board: Board = None
white_move = True
prev_move = None
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

def king_is_checked_after_move(start, end2, king_is_white):
    """
    NOTE: Temporarily makes changes to the board
    """
    king_loc = -1
    curr_end = board[end2]
    board[end2], board[start] = board[start], Piece.Empty

    for i in range(64):
        if (king_is_white and board[i] == Piece.WhiteKing) or (not king_is_white and board[i] == Piece.BlackKing):
            king_loc = i
            break
    if king_loc == -1: raise Exception("NO KING FOUND ON BOARD!")


    # Go bishops moves
    for offset, max_end in BISHOP_OFFSET_MAP[king_loc]:
        for end in range(king_loc + offset, max_end, offset):
            if not piece_on(end):
                continue

            if king_is_white and (board[end] == Piece.BlackBishop or board[end] == Piece.BlackQueen) or \
                    not king_is_white and (board[end] == Piece.WhiteBishop or board[end] == Piece.WhiteQueen):
                board[start], board[end2] = board[end2], curr_end
                return True
            break

    # Go rooks moves
    for offset, max_end in ROOK_OFFSET_MAP[king_loc]:
        for end in range(king_loc + offset, max_end, offset):
            if not piece_on(end):
                continue
            if king_is_white and (board[end] == Piece.BlackRook or board[end] == Piece.BlackQueen) or \
                    not king_is_white and (board[end] == Piece.WhiteRook or board[end] == Piece.WhiteQueen):
                board[start], board[end2] = board[end2], curr_end
                return True
            break
    # Go knights moves
    for end in KNIGHT_MOVE_MAP[king_loc]:
        if king_is_white and (board[end] == Piece.BlackKnight) or \
                not king_is_white and (board[end] == Piece.WhiteKnight):
            board[start], board[end2] = board[end2], curr_end
            return True

    # Go kings moves
    for offset, max_end in QUEEN_OFFSET_MAP[king_loc]:
        for end in range(king_loc + offset, max_end, offset):
            if king_is_white and board[end] == Piece.BlackKing or not king_is_white and board[end] == Piece.WhiteKing:
                board[start], board[end2] = board[end2], curr_end
                return True
            break

    # Go pawns moves
    direction = -8 if king_is_white else +8
    if (king_loc % 8 != 7) and (board[king_loc + direction + 1] == Piece.WhitePawn and not king_is_white and king_loc + direction + 1 < 64 or \
            board[king_loc + direction + 1] == Piece.BlackPawn and king_is_white and king_loc + direction + 1 >= 0):
        board[start], board[end2] = board[end2], curr_end
        return True
    if (king_loc % 8 != 0) and (board[king_loc + direction - 1] == Piece.BlackPawn and king_is_white and king_loc + direction - 1 >= 0 or \
            board[king_loc + direction - 1] == Piece.WhitePawn and not king_is_white and king_loc + direction - 1 < 64):
        board[start], board[end2] = board[end2], curr_end
        return True

    # Castling is little bit more weird

    # revert the changes made
    board[start], board[end2] = board[end2], curr_end

    return False

    

def compute_all_legal_moves():
    """Computes all legal moves possible from the side whos turn it is currently"""
    legal_moves.clear()

    # TODO! Invalidate moves if king is under check after making the move
    for start in range(64):        
        if not target_piece_color_is_correct(start): continue
        if board[start] in (Piece.WhiteBishop, Piece.BlackBishop):
            for offset, max_end in BISHOP_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                        continue
                    if not target_piece_color_is_correct(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhiteRook, Piece.BlackRook):
            for offset, max_end in ROOK_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                        continue
                    if not target_piece_color_is_correct(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhiteQueen, Piece.BlackQueen):
            for offset, max_end in QUEEN_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                        continue
                    if not target_piece_color_is_correct(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhiteKnight, Piece.BlackKnight):
            for end in KNIGHT_MOVE_MAP[start]:
                if not piece_on(end):
                    if not king_is_checked_after_move(start, end, white_move):
                        legal_moves.append((start, end))
                    continue
                if not target_piece_color_is_correct(end):
                    if not king_is_checked_after_move(start, end, white_move):
                        legal_moves.append((start, end))

        elif board[start] in (Piece.WhiteKing, Piece.BlackKing):
            # TODO!
            # Need to check for castling
            for offset, max_end in QUEEN_OFFSET_MAP[start]:
                for end in range(start + offset, max_end, offset):
                    if not piece_on(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                        break # We can only move like one square at a time
                    if not target_piece_color_is_correct(end):
                        if not king_is_checked_after_move(start, end, white_move):
                            legal_moves.append((start, end))
                    break

        elif board[start] in (Piece.WhitePawn, Piece.BlackPawn):
            # TODO! Need to handle promotion
            # TODO! Need to check for empassant
            direction = -8 if white_move else +8
            if not piece_on(start + direction):
                if not king_is_checked_after_move(start, start + direction, white_move):
                    legal_moves.append((start, start + direction))
                
            if ((white_move and start//8 == 6) or (not white_move and start//8 == 1)) and not piece_on(start + direction) and not piece_on(start + direction*2):
                if not king_is_checked_after_move(start, start + direction*2, white_move):
                    legal_moves.append((start, start + direction*2))

            if (start%8 != 7) and piece_on(start + direction + 1) and not target_piece_color_is_correct(start + direction + 1):
                if not king_is_checked_after_move(start, start + direction + 1, white_move):
                    legal_moves.append((start, start + direction + 1))

            if (start%8 != 0) and piece_on(start + direction - 1) and not target_piece_color_is_correct(start + direction - 1):
                if not king_is_checked_after_move(start, start + direction - 1, white_move):
                    legal_moves.append((start, start + direction - 1))

EMPTY_THEATRICS = tuple(Theatrics.none for _ in range(64))
def _reset_theaatrics():
    board.theatrics.clear()
    board.theatrics.extend(EMPTY_THEATRICS)
    if prev_move is not None:
        board.theatrics[prev_move[0]] = Theatrics.highlight
        board.theatrics[prev_move[1]] = Theatrics.highlight

def _add_clicked_piece_theatrics():
    if target_piece_color_is_correct(prev_clicked_square):
        board.theatrics[prev_clicked_square] = Theatrics.target
        for end in (j for i,j in legal_moves if i == prev_clicked_square):
            board.theatrics[end] = Theatrics.marked

def handle_click(loc):
    global prev_clicked_square, white_move, prev_move

    if prev_clicked_square == loc:
        prev_clicked_square = None
        _reset_theaatrics()
        return False, True

    if prev_clicked_square is not None and target_piece_color_is_correct(prev_clicked_square):
        if (prev_clicked_square, loc) not in legal_moves:
            _reset_theaatrics()
            prev_clicked_square = loc
            _add_clicked_piece_theatrics()
            return False, True

        
        board[prev_clicked_square], board[loc] = 0, board[prev_clicked_square]
        prev_move = (prev_clicked_square, loc)
        _reset_theaatrics()


        white_move = not white_move
        prev_clicked_square = None
        compute_all_legal_moves()
        return True, True
    else:
        if prev_clicked_square is not None:
            _reset_theaatrics()
        prev_clicked_square = loc
        _add_clicked_piece_theatrics()
        return False, True
    
