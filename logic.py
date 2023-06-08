from consts import Piece

board = None
white_move = True
prev_clicked_square = None


def init_logix(_board):
    global board
    board = _board

def target_piece_color_is_correct():
    return prev_clicked_square is not None and \
        (
            (white_move and board[prev_clicked_square] >= Piece.WhitePawn and board[prev_clicked_square] <= Piece.WhiteKing) or \
            (not white_move and board[prev_clicked_square] >= Piece.BlackPawn and board[prev_clicked_square] <= Piece.BlackKing)
        )


def handle_click(loc):
    global prev_clicked_square, white_move

    if prev_clicked_square is not None:
        if not target_piece_color_is_correct():
            prev_clicked_square = None
            return False

        board[prev_clicked_square], board[loc] = 0, board[prev_clicked_square]
        white_move = not white_move
        prev_clicked_square = None
        return True
    else:
        prev_clicked_square = loc
        return False
    
