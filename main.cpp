#define _WIN32_WINNT 0x0501

#include "definitions.cpp"
#include "gui.cpp"
#include "engine.cpp"
#include "board.cpp"
#include "mingw.shared_mutex.h"

void handleUserMoves(Board* board, shared_mutex* boardMutex, Definitions::Theatric* theatrics);

using namespace std::chrono_literals;
int main(){
    Board board;
    shared_mutex boardMutex;
    Definitions::Theatric* theatrics = new Definitions::Theatric[64]{Definitions::Theatrics::none};
    
    GUI::init(&board, &boardMutex, theatrics);
    Engine::init(&board, &boardMutex);
    
    std::this_thread::sleep_for(1s); // Wait for the board and engine to finish initialization

    handleUserMoves(&board, &boardMutex, theatrics);

    Engine::terminate();
    GUI::terminate();

    std::this_thread::sleep_for(1s); // Wait for the shit to terminate
    
    return 0;
};

void handleUserMoves(Board* board, shared_mutex* boardMutex, Definitions::Theatric* theatrics)
{
    Square prevClickedSquare = Definitions::NULL_SQUARE;

    auto resetTheatrics = [theatrics]{
        for(int i=0;i<64;i++)
        {
            theatrics[i] = Definitions::Theatrics::none;
        }
    };

    auto addClickedSquareTheatrics = [theatrics, &prevClickedSquare, board]{
        if (prevClickedSquare == NULL_SQUARE){return;}
        if (board->pieceColorIsCorrect(prevClickedSquare)){
            theatrics[prevClickedSquare] = Definitions::Theatrics::target;
            // for end in (j for i,j,_ in board.legal_moves if i == prev_clicked_square):
            //     theatrics[end] = Theatrics.marked
        }
    };
    
    while (GUI::isRunning)
    {
        GUI::clickedSquareQMutex.lock();
        if (GUI::clickedSquareQ.empty()){
            GUI::clickedSquareQMutex.unlock();

            GUI::clickedSquareSignal.wait(); // Signal is set by GUI, whenever the board is clicked
            GUI::clickedSquareSignal.reset();
            continue;
        }

        Definitions::Square clickedSquare = GUI::clickedSquareQ.front();
        GUI::clickedSquareQ.pop();
        
        GUI::clickedSquareQMutex.unlock();

        // Handle the click
        boardMutex->lock();

        if (prevClickedSquare == clickedSquare){ // Case where we click on same square
            prevClickedSquare = NULL_SQUARE;
            resetTheatrics();

            boardMutex->unlock();
            GUI::requestRender();
            continue;
        }

        // Case where we select first piece (i.e. previously clicked square was invalid)
        if (prevClickedSquare == NULL_SQUARE || !board->pieceColorIsCorrect(prevClickedSquare)){
            if (prevClickedSquare != NULL_SQUARE){resetTheatrics();}
            prevClickedSquare = clickedSquare;
            addClickedSquareTheatrics();
            
            boardMutex->unlock();
            GUI::requestRender();
            continue;
        }
        
        // prevClickedSquare was a valid piece and now we have to check if the move is possible
        bool found = false;
        for (auto move: board->legalMoves){
            if (move.start == prevClickedSquare && move.end == clickedSquare){
                found = true;
                break;
            }
        }
        if (!found){ // If move was illegal
            resetTheatrics();
            prevClickedSquare = clickedSquare;
            addClickedSquareTheatrics();
            
            boardMutex->unlock();
            GUI::requestRender();
            continue;
        }
        
        // Proposed move is legal, now just need additional input in the case of promotion otherwise just make move
        // if (!tryingToPromote){
        //     board.makeMove();
        //     board.computeAllLegalMoves();
        //     prevClickedSquare = NULL_SQUARE;
        //     resetTheatrics();
        //     
        //     boardMutex->unlock();
        //     GUI::requestRender();
        //     continue;
        // }

        // They are trying to promote
        // promotionPiece = getPromotionPiece
        // if promotionPiece == NULL{ // Basically just cancel move
        //     prevClickedSquare = NULL_SQUARE;
        //     resetTheatrics();

        //     boardMutex->unlock();
        //     GUI::requestRender();
        //     continue;
        // }

        // board.makeMove({start, end, promotionPiece});
        // board.computeAllLegalMoves();
        // prevClickedSquare = NULL_SQUARE;
        // resetTheatrics();
        
        // boardMutex->unlock();
        // GUI::requestRender();
        // continue;
    }
}
