BOARD = 0

from enum import IntEnum, auto

class Piece(IntEnum):
    BlackPawn   = auto()
    BlackKnight = auto()
    BlackBishop = auto()
    BlackRook   = auto()
    BlackQueen  = auto()
    BlackKing   = auto()

    WhitePawn   = auto()
    WhiteKnight = auto()
    WhiteBishop = auto()
    WhiteRook   = auto()
    WhiteQueen  = auto()
    WhiteKing   = auto()

class EventTypes(IntEnum):
    click = auto()

class Theatrics(IntEnum):
    highlight = auto() # highlights the square (to show previous move)
    marked = auto() # marks a square (to show valid moves)
    target = auto() # shows that the square was clicked
