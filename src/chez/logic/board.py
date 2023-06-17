from chez.general.definitions import Position, Pieces, Colors, Square, _Piece, _ColoredPiece, _Color, Move
from .offsetMaps import BISHOP_OFFSET_MAP, ROOK_OFFSET_MAP, QUEEN_OFFSET_MAP, KNIGHT_MOVE_MAP

class TemporaryMoveCreator:
    def __init__(self, position: Position) -> None:
        self.position = position
        self.move = None
        self.currEnd = None

    def setMove(self, start, end):
        self.move = (start, end)
        
    def __enter__(self, *_):
        if self.move is None:
            raise Exception("Move is not set, temporary move cannot be made")

        self.currEnd = self.position[self.move[1]]
        self.position[self.move[1]] = self.position[self.move[0]]
        self.position[self.move[0]] = Pieces.Empty

    def __exit__(self, *_):
        self.position[self.move[0]] = self.position[self.move[1]]
        self.position[self.move[1]] = self.currEnd        
        self.move = None

class Board:
    def __init__(self) -> None:
        self.position: Position = [
            Colors.Black|Pieces.Rook  , Colors.Black|Pieces.Knight, Colors.Black|Pieces.Bishop, Colors.Black|Pieces.Queen , Colors.Black|Pieces.King  , Colors.Black|Pieces.Bishop, Colors.Black|Pieces.Knight, Colors.Black|Pieces.Rook  ,
            Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  , Colors.Black|Pieces.Pawn  ,
            Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty ,
            Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty , Colors.Black|Pieces.Empty ,
            Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty ,
            Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty , Colors.White|Pieces.Empty ,
            Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  , Colors.White|Pieces.Pawn  ,
            Colors.White|Pieces.Rook  , Colors.White|Pieces.Knight, Colors.White|Pieces.Bishop, Colors.White|Pieces.Queen , Colors.White|Pieces.King  , Colors.White|Pieces.Bishop, Colors.White|Pieces.Knight, Colors.White|Pieces.Rook  ,
        ]

        self._temporary_move_creator = TemporaryMoveCreator(self.position)

        self.is_white_move = True
        """Set to true if it is currently white's turn"""
        self.legal_moves: list[Move] = []
        """List of all legal moves at the current state of the board"""
        self.prev_move: tuple[Square, Square] = None
        """Keeps track of the last move made (for en passant)"""

        self.white_can_castle_short = True
        """Set to true if white can castle kingside"""
        self.white_can_castle_long = True
        """Set to true if white can castle queenside"""
        self.black_can_castle_short = True
        """Set to true if black can castle kingside"""
        self.black_can_castle_long = True
        """Set to true if black can castle queenside"""

    def _temporary_move(self, start, end):
        self._temporary_move_creator.setMove(start, end)
        return self._temporary_move_creator

    def colored_piece_on(self, square: Square) -> _ColoredPiece:
        """Returns the colored piece present on the square"""
        return self.position[square]
    

    def piece_on(self, square: Square) -> _Piece:
        """Returns the _Piece on the square"""
        return self.colored_piece_on(square) >> 1 << 1
    
    def piece_color_on(self, square: Square) -> _Color:
        """
        Returns the _Color of the piece on the square
        NOTE: If there is no piece on the color is not well defined
        """
        return self.colored_piece_on(square) & 0b1

    def piece_color_is_correct(self, square: Square, color_is_white = None):
        """
        Returns true if its white's move and the piece on the square is white (same for black)
        If color_is_white is set to None, `self.is_white_move` is used instead
        """
        color_is_white = color_is_white if color_is_white is not None else self.is_white_move
        return self.piece_is_on(square) and (
                (self.is_white_move and self.piece_color_on(square) == Colors.White) or 
                (not self.is_white_move and self.piece_color_on(square) == Colors.Black)
            )

    def piece_is_on(self, square: Square) -> bool:
        """Returns true if a piece is present on the square"""
        return self.piece_on(square) != Pieces.Empty
    
    def compute_all_legal_moves(self):
        """Updates the current legal moves from the given state of the board"""
        self.legal_moves.clear()

        for possible_start in range(64):
            if not self.piece_color_is_correct(possible_start): continue

            if self.piece_on(possible_start) == Pieces.Bishop:
                for offset, max_end in BISHOP_OFFSET_MAP[possible_start]:
                    for end in range(possible_start + offset, max_end, offset):
                        if not self.piece_is_on(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                            continue

                        if not self.piece_color_is_correct(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                        break


            elif self.piece_on(possible_start) == Pieces.Rook:
                for offset, max_end in ROOK_OFFSET_MAP[possible_start]:
                    for end in range(possible_start + offset, max_end, offset):
                        if not self.piece_is_on(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                            continue

                        if not self.piece_color_is_correct(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                        break

            elif self.piece_on(possible_start) == Pieces.Queen:
                for offset, max_end in QUEEN_OFFSET_MAP[possible_start]:
                    for end in range(possible_start + offset, max_end, offset):
                        if not self.piece_is_on(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                            continue

                        if not self.piece_color_is_correct(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                        break

            elif self.piece_on(possible_start) == Pieces.King:
                for offset, max_end in QUEEN_OFFSET_MAP[possible_start]:
                    for end in range(possible_start + offset, max_end, offset):
                        if not self.piece_is_on(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                            break

                        if not self.piece_color_is_correct(end):
                            if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                                self.legal_moves.append((possible_start, end, None))
                        break

                if self.white_can_castle_long and self.is_white_move:
                    if self.piece_on(60) == Pieces.King and \
                            not self.piece_is_on(57) and not self.piece_is_on(58) and not self.piece_is_on(59) and \
                            not self.king_is_checked(self.is_white_move) and \
                            self.king_is_not_checked_after_move(60, 59, self.is_white_move) and \
                            self.king_is_not_checked_after_move(60, 58, self.is_white_move):
                        self.legal_moves.append((60, 58, None))
                if self.white_can_castle_short and self.is_white_move:
                    if self.piece_on(60) == Pieces.King and \
                            not self.piece_is_on(61) and not self.piece_is_on(62) and \
                            not self.king_is_checked(self.is_white_move) and \
                            self.king_is_not_checked_after_move(60, 61, self.is_white_move) and \
                            self.king_is_not_checked_after_move(60, 62, self.is_white_move):
                        self.legal_moves.append((60, 62, None))
                if self.black_can_castle_long and not self.is_white_move:
                    if self.piece_on(4) == Pieces.King and \
                            not self.piece_is_on(1) and not self.piece_is_on(2) and not self.piece_is_on(3) and \
                            not self.king_is_checked(self.is_white_move) and \
                            self.king_is_not_checked_after_move(4, 3, self.is_white_move) and \
                            self.king_is_not_checked_after_move(4, 2, self.is_white_move):
                        self.legal_moves.append((4, 2, None))
                if self.black_can_castle_short and not self.is_white_move:
                    if self.piece_on(4) == Pieces.King and \
                            not self.piece_is_on(5) and not self.piece_is_on(6) and \
                            not self.king_is_checked(self.is_white_move) and \
                            self.king_is_not_checked_after_move(4, 5, self.is_white_move) and \
                            self.king_is_not_checked_after_move(4, 6, self.is_white_move):
                        self.legal_moves.append((4, 6, None))

            elif self.piece_on(possible_start) == Pieces.Knight:
                for end in KNIGHT_MOVE_MAP[possible_start]:
                    if self.piece_color_is_correct(end):continue
                    if self.king_is_not_checked_after_move(possible_start, end, self.is_white_move):
                        self.legal_moves.append((possible_start, end, None))

            elif self.piece_on(possible_start) == Pieces.Pawn:
                direction = -8 if self.is_white_move else +8
                
                pieces = (Pieces.Queen, Pieces.Rook, Pieces.Bishop, Pieces.Knight, ) if not 0 < (possible_start + direction) // 8 < 7 else (None,)
                
                if not self.piece_is_on(possible_start + direction) and self.king_is_not_checked_after_move(possible_start, possible_start + direction, self.is_white_move):
                    if self.king_is_not_checked_after_move(possible_start, possible_start + direction, self.is_white_move):
                        for piece in pieces:self.legal_moves.append((possible_start, possible_start + direction, piece))
                    
                if ((self.is_white_move and possible_start//8 == 6) or (not self.is_white_move and possible_start//8 == 1)) and not self.piece_is_on(possible_start + direction) and not self.piece_is_on(possible_start + direction*2) and self.king_is_not_checked_after_move(possible_start, possible_start + direction*2, self.is_white_move):
                    if self.king_is_not_checked_after_move(possible_start, possible_start + direction*2, self.is_white_move):
                        for piece in pieces:self.legal_moves.append((possible_start, possible_start + direction*2, piece))

                if (possible_start%8 != 7) and self.piece_is_on(possible_start + direction + 1) and not self.piece_color_is_correct(possible_start + direction + 1) and self.king_is_not_checked_after_move(possible_start, possible_start + direction + 1, self.is_white_move):
                    if self.king_is_not_checked_after_move(possible_start, possible_start + direction + 1, self.is_white_move):
                        for piece in pieces:self.legal_moves.append((possible_start, possible_start + direction + 1, piece))

                if (possible_start%8 != 0) and self.piece_is_on(possible_start + direction - 1) and not self.piece_color_is_correct(possible_start + direction - 1) and self.king_is_not_checked_after_move(possible_start, possible_start + direction - 1, self.is_white_move):
                    if self.king_is_not_checked_after_move(possible_start, possible_start + direction - 1, self.is_white_move):
                        for piece in pieces:self.legal_moves.append((possible_start, possible_start + direction - 1, piece))
                
                # en passant
                if (possible_start%8 != 7) and self.piece_on(possible_start + 1) == Pieces.Pawn and not self.piece_color_is_correct(possible_start + 1) and (
                    self.is_white_move and self.prev_move == ((possible_start+1)%8 + (1*8), (possible_start+1)%8 + (3*8)) or \
                    not self.is_white_move and self.prev_move == ((possible_start+1)%8 + (6*8), (possible_start+1)%8 + (4*8))
                ):
                    xs, self.position[possible_start + 1] = self.position[possible_start + 1], Pieces.Empty
                    if self.king_is_not_checked_after_move(possible_start, possible_start + direction + 1, self.is_white_move):
                        self.legal_moves.append((possible_start, possible_start + direction + 1, None))
                    self.position[possible_start + 1] = xs

                if (possible_start%8 != 0) and self.piece_on(possible_start - 1) == Pieces.Pawn and not self.piece_color_is_correct(possible_start - 1) and (
                    self.is_white_move and self.prev_move == ((possible_start-1)%8 + (1*8), (possible_start-1)%8 + (3*8)) or \
                    not self.is_white_move and self.prev_move == ((possible_start-1)%8 + (6*8), (possible_start-1)%8 + (4*8))
                ):
                    xs, self.position[possible_start - 1] = self.position[possible_start - 1], Pieces.Empty
                    if self.king_is_not_checked_after_move(possible_start, possible_start + direction - 1, self.is_white_move):
                        self.legal_moves.append((possible_start, possible_start + direction - 1, None))
                    self.position[possible_start - 1] = xs

            else:
                raise Exception("UNREACHABLE!")


    def king_is_checked(self, king_is_white: bool):
        """Returns true if the target king is checked at the current position"""
        king_loc = -1
        for i in range(64):
            if (king_is_white and self.position[i] == Colors.White|Pieces.King) or (not king_is_white and self.position[i] == Colors.Black|Pieces.King):
                king_loc = i
                break
        if king_loc == -1: raise Exception("NO KING FOUND ON BOARD!")

        # Go bishops moves
        for offset, max_end in BISHOP_OFFSET_MAP[king_loc]:
            for end in range(king_loc + offset, max_end, offset):
                if not self.piece_is_on(end):
                    continue

                if self.piece_on(end) in (Pieces.Bishop, Pieces.Queen) and not self.piece_color_is_correct(end, color_is_white=king_is_white):
                    return True
                break

        # Go rooks moves
        for offset, max_end in ROOK_OFFSET_MAP[king_loc]:
            for end in range(king_loc + offset, max_end, offset):
                if not self.piece_is_on(end):
                    continue

                if self.piece_on(end) in (Pieces.Rook, Pieces.Queen) and not self.piece_color_is_correct(end, color_is_white=king_is_white):
                    return True
                break
        
        # Go knights moves
        for end in KNIGHT_MOVE_MAP[king_loc]:
            if self.piece_on(end) == Pieces.Knight and not self.piece_color_is_correct(end, color_is_white=king_is_white):
                return True

        # Go kings moves
        for offset, max_end in QUEEN_OFFSET_MAP[king_loc]:
            for end in range(king_loc + offset, max_end, offset):
                if self.piece_on(end) == Pieces.King and not self.piece_color_is_correct(end, color_is_white=king_is_white):
                    return True
                break

        # Go pawns moves
        direction = -8 if king_is_white else +8
        if (king_loc % 8 != 7) and -1 < king_loc + direction + 1 < 64 and self.piece_on(king_loc + direction + 1) == Pieces.Pawn and not self.piece_color_is_correct(king_loc + direction + 1, color_is_white=king_is_white):
            return True
        if (king_loc % 8 != 0) and -1 < king_loc + direction - 1 < 64 and self.piece_on(king_loc + direction - 1) == Pieces.Pawn and not self.piece_color_is_correct(king_loc + direction - 1, color_is_white=king_is_white):
            return True

        return False

    def king_is_not_checked_after_move(self, start: Square, end: Square, king_is_white: bool):
        """Returns true if the target king will not be checked after making the move"""
        with self._temporary_move(start, end):
            return not self.king_is_checked(king_is_white)

    def make_move(self, move: Move):
        start, end, promotion_piece = move

        if self.piece_on(start) == Pieces.King:
            if self.black_can_castle_long and (start, end) == (4, 2):
                self.position[0], self.position[3] = self.position[3], self.position[0]
            elif self.black_can_castle_short and (start, end) == (4, 6):
                self.position[5], self.position[7] = self.position[7], self.position[5]
            elif self.white_can_castle_long and (start, end) == (60, 58):
                self.position[56], self.position[59] = self.position[59], self.position[56]
            elif self.white_can_castle_short and (start, end) == (60, 62):
                self.position[63], self.position[61] = self.position[61], self.position[63]

            if self.piece_color_on(start) == Colors.White:self.white_can_castle_long = self.white_can_castle_short = False
            if self.piece_color_on(start) == Colors.Black:self.black_can_castle_long = self.black_can_castle_short = False

        elif self.piece_on(start) == Pieces.Rook:
            if self.piece_color_on(start) == Colors.Black:
                if start == 0:
                    self.black_can_castle_long = False
                elif start == 7:
                    self.black_can_castle_short = False        
            else:
                if start == 56:
                    self.white_can_castle_long = False
                elif start == 63:
                    self.white_can_castle_short = False

        if self.piece_on(start) == Pieces.Pawn and (start%8 != end%8) and not self.piece_on(end): # en passant bro
            self.position[(end%8) - (start%8) + start] = Pieces.Empty
        self.position[start], self.position[end] = Pieces.Empty, self.position[start]
        self.is_white_move = not self.is_white_move
        self.prev_move = (start, end)

        # promotion check
        if promotion_piece is not None:
            self.position[end] = self.piece_color_on(end)|promotion_piece