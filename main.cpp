#define _WIN32_WINNT 0x0501

#include "definitions.cpp"
#include "gui.cpp"
#include "engine.cpp"
#include "board.cpp"

using namespace std::chrono_literals;
int main(){
    GUI::init();
    Engine::init();

    // std::this_thread::sleep_for(10000ms);

    GUI::_thread.join();
    Engine::terminate();
    
    return 0;
};