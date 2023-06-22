from __future__ import annotations
from typing import TYPE_CHECKING
from chez.general import Colors

if TYPE_CHECKING:
    from chez.logic import Board

def naive_evaluate(board: Board):
    white_sum = 0
    black_sum = 0
    for square in range(64):
        if not board.piece_is_on(square):continue
        if board.piece_color_on(square) == Colors.Black:
            black_sum += board.piece_on(square)
        else:
            white_sum += board.piece_on(square)

    return white_sum - black_sum
