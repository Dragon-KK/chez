#define _WIN32_WINNT 0x0501

#include "definitions.cpp"
#include "gui.cpp"
#include "engine.cpp"
#include "board.cpp"

#include "mingw.shared_mutex.h"


void handleClick(Square clickedSquare);
void handleUserMoves(Board* board, shared_mutex* boardMutex);

using namespace std::chrono_literals;
int main(){
    Board board;
    shared_mutex boardMutex;
    
    GUI::init(&board, &boardMutex);
    Engine::init(&board, &boardMutex);
    
    std::this_thread::sleep_for(1s); // Wait for the board and engine to finish initialization

    handleUserMoves(&board, &boardMutex);

    GUI::terminate();
    Engine::terminate();
    
    return 0;
};

void handleUserMoves(Board* board, shared_mutex* boardMutex)
{
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
        board->position[clickedSquare] = board->position[rand() % 9];
        boardMutex->unlock();

        GUI::requestRender();
    }
}
