#pragma once
#include "mingw.thread.h"

namespace Engine{
    std::thread _thread;
    bool isRunning = false;

    void _run(){
        
    }

    void init(){
        Engine::_thread = std::thread(Engine::_run);
    }

    void terminate(){
        Engine::isRunning = false;
        Engine::_thread.join();
    }
};