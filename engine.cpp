#pragma once
#include "mingw.thread.h"
#include "mingw.shared_mutex.h"
#include <chrono>
#include <iostream>

using namespace std::chrono_literals;
namespace Engine{
    std::thread _thread;
    bool isRunning = false;

    namespace External{
        Board* board;
        std::shared_mutex* boardMutex;
    }

    void terminate(){
        Engine::isRunning = false;
        Engine::_thread.join();
    }

    void _run(){
        Engine::isRunning = true;
        while (Engine::isRunning){
            std::this_thread::sleep_for(1s);
            // Engine::External::boardMutex->lock();
            // Engine::External::board->position[31] = Engine::External::board->position[rand() % 9];
            // Engine::External::boardMutex->unlock();
        }
    }

    void init(Board* _board, std::shared_mutex* _boardMutex){
        Engine::External::board = _board;
        Engine::External::boardMutex = _boardMutex;
        Engine::_thread = std::thread(Engine::_run);
    }
};