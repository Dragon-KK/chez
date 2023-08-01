#pragma once
#include "definitions.cpp"
#define OUT
#define MAX_LEGAL_MOVES_LENGTH 218
// https://www.chess.com/forum/view/fun-with-chess/what-chess-position-has-the-most-number-of-possible-moves?page=2

using namespace Definitions;
class Board{
public:
    /**
     * Array containing all the legal moves for a given state of the board
     * @note This array must be recalculated after every move
    */
    Move legalMoves[MAX_LEGAL_MOVES_LENGTH]{NULL_MOVE};
    int legalMovesLength = 0;
    /**
     * Keeps track of the previous move made (for en passent checks)
    */
    Move previousMove = NULL_MOVE;

    /**
     * Keeps track of which color's turn it is currently
    */
    Color turn = Colors::White;
    /**
     * Use `&` allong with Castles::* to make required check
    */
    CastleInformation castleState = Castles::BlackKingside | Castles::BlackQueenside | Castles::WhiteQueenside | Castles::WhiteKingside;
    
    /**
     * Array containing information about the current position
    */
    ColoredPiece position[64] = {
        (ColoredPiece)(Colors::Black|Pieces::Rook)  , (ColoredPiece)(Colors::Black|Pieces::Knight), (ColoredPiece)(Colors::Black|Pieces::Bishop), (ColoredPiece)(Colors::Black|Pieces::Queen) , (ColoredPiece)(Colors::Black|Pieces::King)  , (ColoredPiece)(Colors::Black|Pieces::Bishop), (ColoredPiece)(Colors::Black|Pieces::Knight), (ColoredPiece)(Colors::Black|Pieces::Rook)  ,
        (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  , (ColoredPiece)(Colors::Black|Pieces::Pawn)  ,
        (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) ,
        (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) ,
        (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) ,
        (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) , (ColoredPiece)(Colors::Black|Pieces::Empty) ,
        (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  , (ColoredPiece)(Colors::White|Pieces::Pawn)  ,
        (ColoredPiece)(Colors::White|Pieces::Rook)  , (ColoredPiece)(Colors::White|Pieces::Knight), (ColoredPiece)(Colors::White|Pieces::Bishop), (ColoredPiece)(Colors::White|Pieces::Queen) , (ColoredPiece)(Colors::White|Pieces::King)  , (ColoredPiece)(Colors::White|Pieces::Bishop), (ColoredPiece)(Colors::White|Pieces::Knight), (ColoredPiece)(Colors::White|Pieces::Rook)  ,
    };

    /**
     * Gets the ColoredPiece on the given square
     * 
     * @param square The desired square to get
     * 
     * @warning The function does not check if the square is valid (i.e. in [0..64])
    */
    ColoredPiece getColoredPieceOn(Square& square){
        return this->position[square];
    }

    /**
     * Gets the Piece on the given square
     * 
     * @param square The desired square to get
     * 
     * @warning The function does not check if the square is valid (i.e. in [0..64])
    */
    Piece getPieceOn(Square& square){
        return this->position[square] >> 1 << 1;
    }

    /**
     * Gets the color of the piece on the given square
     * 
     * @param square The desired square to get
     * 
     * @note The color of an empty square is not well defined
     * 
     * @warning The function does not check if a piece exists on the square
     * @warning The function does not check if the square is valid (i.e. in [0..64])
    */
    Color getColorOn(Square& square){
        return this->position[square] & 0b1;
    }

    /**
     * Checks whether a piece is present on the given square
     * 
     * @param square The desired square to check
     * 
     * @warning The function does not check if the square is valid (i.e. in [0..64])
    */
    bool pieceIsOn(Square& square){
        return (this->position[square] >> 1 << 1) != Pieces::Empty;
    }

    /**
     * Checks whether a piece is present on the given square and the color of the piece on it is the same as board.turn
     * 
     * @param square The desired square to check
     * 
     * @warning The function does not check if the square is valid (i.e. in [0..64])
    */
    bool pieceColorIsCorrect(Square& square){
        return pieceIsOn(square) && (getColorOn(square) == turn);
    }

    void somFunction(OUT bool& isdC){
        isdC = true;

    }


    void recalculateLegalMoves(){
        for (int i=0; i<legalMovesLength; i++) {legalMoves[i] = NULL_MOVE;}
        legalMovesLength = 0;
        
        // Easily look for valid king moves (same way as we did previously)

        bool isDoubleChecked = false;
        somFunction(isDoubleChecked);
        // If we are not checked currently, 
        //  - Find all the pinned pieces (Store direction of the pin, sliding pieces can only move in direction of pin, knigths cannot move)
        //  - Now it is assured that all other pieces can move pretty much however they want to (without worrying about checks)
        //  Peaaaaaaaaace

        // If we are checked:
        //  - King moves we do the same
        //  - If we are double checked, only the king can move
        //  - Otherwise store the direction of the check, our piece has to move to same line (slope same scene)
        
    }
};