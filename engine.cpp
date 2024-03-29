#pragma once
#ifdef _WIN32
    #include "mingw.thread.h"
    #include "mingw.shared_mutex.h"
#else
    #include <thread>
    #include <shared_mutex>
#endif
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

    void terminate(){
        Engine::isRunning = false;
        Engine::_thread.join();
    }
};