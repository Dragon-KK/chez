from .gui import ChezGui
from .logic import Board
from .general import Square
from .gui.consts import Targets, EventTypes, Theatrics
from .general import Pieces, Colors
from .engines import PrunedMinimaxEngine
from .engines.engine import CancellationToken

ct = CancellationToken()

# TODO! Investigate the lag that occurs whenever a move is made
# It is prolly due to calculation of all legal moves


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("COULD NOT SET DPI AWARENESS!")


prev_clicked_square: Square = None

board = Board()
theatrics: list[Theatrics] = []

engine = PrunedMinimaxEngine()
# engine.start()

board.compute_all_legal_moves()

engine.update_board(board)
# engine.begin_evaluation()
engine.evaluate(2, ct)

EMPTY_THEATRICS = tuple(Theatrics.none for _ in range(64))
def _reset_theatrics():
    theatrics.clear()
    theatrics.extend(EMPTY_THEATRICS)
    if board.prev_move is not None:
        theatrics[board.prev_move[0]] = Theatrics.highlight
        theatrics[board.prev_move[1]] = Theatrics.highlight

def _add_clicked_piece_theatrics():
    if prev_clicked_square is None:return
    if board.piece_color_is_correct(prev_clicked_square):
        theatrics[prev_clicked_square] = Theatrics.target
        for end in (j for i,j,_ in board.legal_moves if i == prev_clicked_square):
            theatrics[end] = Theatrics.marked

_reset_theatrics()

chez = ChezGui(
    position=board.position,
    theatrics=theatrics
)

chez.exec()

def handle_click(square: Square):
    global prev_clicked_square

    if prev_clicked_square == square:
        prev_clicked_square = None
        _reset_theatrics()
        return False, True

    if prev_clicked_square is not None and board.piece_color_is_correct(prev_clicked_square):
        if (prev_clicked_square, square) not in [(i, j) for (i, j, _) in board.legal_moves]:
            _reset_theatrics()
            prev_clicked_square = square
            _add_clicked_piece_theatrics()
            return False, True

        # check for promotion
        if board.piece_on(prev_clicked_square) == Pieces.Pawn and not 0 < square// 8 < 7:
            piece = chez.request_promotion_piece(Colors.White if board.is_white_move else Colors.Black)
            if piece is None:
                _reset_theatrics()
                prev_clicked_square = square
                _add_clicked_piece_theatrics()
                return False, True
            board.make_move((prev_clicked_square, square, piece))
            board.compute_all_legal_moves()
            # engine.abort()
            engine.update_board(board)
            engine.evaluate(2, ct)
        else:
            board.make_move((prev_clicked_square, square, None))
            board.compute_all_legal_moves()
            # engine.abort()
            engine.update_board(board)
            engine.evaluate(2, ct)

        
        prev_clicked_square = None
        
        _reset_theatrics()

        return True, True
    else:
        if prev_clicked_square is not None:
            _reset_theatrics()

        prev_clicked_square = square
        _add_clicked_piece_theatrics()
        return False, True

for event in chez.events:
    if event.target != Targets.Board:
        print("HANDLE THIS")
        continue
    
    if event.type != EventTypes.click:
        print("HANDLE THIS 2")
        continue

    need_to_update_pieces, need_to_update_theatrics = handle_click(event.data)
    if need_to_update_theatrics: chez.updateTheatrics()
    if need_to_update_pieces: chez.updateBoard()
