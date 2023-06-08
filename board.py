from consts import Piece, Theatrics

class Board:
    def __init__(self):
        self.core = [
            Piece.BlackRook  , Piece.BlackKnight, Piece.BlackBishop, Piece.BlackQueen , Piece.BlackKing  , Piece.BlackBishop, Piece.BlackKnight, Piece.BlackRook  ,
            Piece.BlackPawn  , Piece.BlackPawn  , Piece.BlackPawn  , Piece.BlackPawn  , Piece.BlackPawn  , Piece.BlackPawn  , Piece.BlackPawn  , Piece.BlackPawn  ,
            0                , 0                , 0                , 0                , 0                , 0                , 0                , 0                ,
            0                , 0                , 0                , 0                , 0                , 0                , 0                , 0                ,
            0                , 0                , 0                , 0                , 0                , 0                , 0                , 0                ,
            0                , 0                , 0                , 0                , 0                , 0                , 0                , 0                ,
            Piece.WhitePawn  , Piece.WhitePawn  , Piece.WhitePawn  , Piece.WhitePawn  , Piece.WhitePawn  , Piece.WhitePawn  , Piece.WhitePawn  , Piece.WhitePawn  ,
            Piece.WhiteRook  , Piece.WhiteKnight, Piece.WhiteBishop, Piece.WhiteQueen , Piece.WhiteKing  , Piece.WhiteBishop, Piece.WhiteKnight, Piece.WhiteRook  ,
        ]
        self.theatrics = [ ]

    def __getitem__(self, key):
        return self.core[key]

    def __setitem__(self, key, value):
        self.core[key] = value

    def __iter__(self):
        return self.core.__iter__()