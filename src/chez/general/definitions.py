from typing import Annotated
from types import SimpleNamespace

_Color = int
_Piece = int
_ColoredPiece = int
Square = int
Move = tuple[Square, Square, _Piece]

class Colors(SimpleNamespace):
    White = _Color(0b0001)
    Black = _Color(0b0000)

class Pieces(SimpleNamespace):
    Empty  = _Piece(0b0000)
    Pawn   = _Piece(0b0010)
    Knight = _Piece(0b0100)
    Bishop = _Piece(0b0110)
    Rook   = _Piece(0b1000)
    Queen  = _Piece(0b1010)
    King   = _Piece(0b1100)

Position = Annotated[list[_ColoredPiece], 64]
