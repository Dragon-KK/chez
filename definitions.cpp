#pragma once
#include <stdint.h>

namespace Definitions{
    typedef uint8_t Square;
    typedef bool Color;
    typedef uint8_t Piece;
    /**
     * ColoredPiece = Color | Piece
    */
    typedef uint8_t ColoredPiece;
    typedef uint8_t CastleInformation;

    /**
     * @note `promotedPiece` is set to Pieces::Empty if no promotion was made
    */
    struct Move{
        Square start;
        Square end;
        Piece promotedPiece;
    };

    namespace Colors{
        Color Black = 0;
        Color White = 1;
    }

    namespace Pieces{
        Piece Empty  = 0b0000;
        Piece Pawn   = 0b0010;
        Piece Knight = 0b0100;
        Piece Bishop = 0b0110;
        Piece Rook   = 0b1000;
        Piece Queen  = 0b1010;
        Piece King   = 0b1100;
    }

    namespace Castles{
        uint8_t WhiteKingside  = 0b0001;
        uint8_t WhiteQueenside = 0b0010;
        uint8_t BlackKingside  = 0b0100;
        uint8_t BlackQueenside = 0b1000;
    }

    Move NULL_MOVE = {
        0, 0, Pieces::Empty
    };
};
