#pragma once
#define GLEW_STATIC

#include <GL/glew.h>
#ifdef _WIN32
    #include "mingw.thread.h"
    #include "mingw.shared_mutex.h"
#else
    #include <thread>
    #include <shared_mutex>
#endif
#include "logging.cpp"
#include <GLFW/glfw3.h>
#include <string>
#include <queue>
#include "definitions.cpp"
#include "imghelper.cpp"
#include "glHelper.cpp"
#include "shaderHelper.cpp"
#include "vendors/glm/glm.hpp"
#include "vendors/glm/gtc/matrix_transform.hpp"
#include "vendors/glm/gtc/type_ptr.hpp"
#include "board.cpp"
#include "asynch.cpp"

namespace GUI{
    std::thread _thread;
    bool isRunning = false;

    bool renderIsRequested = false;
    shared_mutex renderIsRequestedMutex;
    namespace External{
        Board* board;
        std::shared_mutex* boardMutex;
        Definitions::Theatric* theatrics;
    }

    std::queue<Definitions::Square> clickedSquareQ;
    std::mutex clickedSquareQMutex;
    Signal clickedSquareSignal;

    Shader _shader;
    Texture* _textures;

    glm::mat4 _mvp;

    namespace WindowProperties{
        pair<int, int> size;
    }

    namespace WindowDefaults{
        pair<int, int> size = pair<int, int>{1120, 720};
        std::string title = "MyWindow";
    };

    namespace ShaderPaths{
        std::string vert = "./shaders/vs.vert";
        std::string frag = "./shaders/fs.frag";
    }
    
    GLFWwindow* _window;

    void _calculate_MVP(){
        _mvp = glm::ortho(0.0f, ((float)GUI::WindowProperties::size.first), 0.0f, ((float)GUI::WindowProperties::size.second), -1.0f, 1.0f);
    }

    void render(){
        glfwMakeContextCurrent(GUI::_window);
        glClear(GL_COLOR_BUFFER_BIT);

        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        GUI::_shader.setUniformMatrix4f("mvp", _mvp);
        
        GUI::External::boardMutex->lock_shared();
        for (int i = 0; i < 64; i++){
            GUI::_shader.setUniformInt("tex", GUI::External::board->position[i]);
            GUI::_shader.setUniformInt("square", i);
            GUI::_shader.setUniformInt("theatric", GUI::External::theatrics[i]);
            GL::drawSquare();
        }
        GUI::External::boardMutex->unlock_shared();

        glfwSwapBuffers(GUI::_window);
    }

    void _mouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
    {
        if(button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS) 
        {
            double xpos, ypos;
            glfwGetCursorPos(window, &xpos, &ypos);

            if (xpos < 80 || xpos > (80 + (70*8))){return;}

            int top = (GUI::WindowProperties::size.second/2) - 280;
            if (ypos < top || ypos > (top + (70*8))){return;}

            int xSquare = (xpos - 80) / 70;
            int ySquare = ((ypos - top) / 70);

            GUI::clickedSquareQMutex.lock();
            GUI::clickedSquareQ.push(xSquare + 8*(ySquare));            
            GUI::clickedSquareQMutex.unlock();

            GUI::clickedSquareSignal.set();
        }
    }

    void _windowSizeCallback(GLFWwindow* _window, int width, int height) {
        glViewport(0, 0, width, height);
        GUI::WindowProperties::size.first = width;
        GUI::WindowProperties::size.second = height;
        GUI::_calculate_MVP();
        GUI::render();
    }

    void _run(){
        GUI::WindowProperties::size.first = GUI::WindowDefaults::size.first;
        GUI::WindowProperties::size.second = GUI::WindowDefaults::size.second;
        GUI::_window = GL::initialize(GUI::WindowDefaults::size, GUI::WindowDefaults::title);

        if (!GUI::_window){return;}

        GUI::isRunning = true;
        _textures = GL::createTextures();
                
        glfwSetWindowSizeCallback(GUI::_window, GUI::_windowSizeCallback);
        glfwSetMouseButtonCallback(GUI::_window, GUI::_mouseButtonCallback);
        glfwSwapInterval(1); // Limits the fps at refresh rate of system

        GUI::_shader.loadProgramByPath(
            GUI::ShaderPaths::vert,
            GUI::ShaderPaths::frag
        );
        GUI::_shader.use();
        
        GL::createStaticSquareVertexBuffer();
        GL::createStaticSquareIndexBuffer();

        GUI::_calculate_MVP();

        GUI::render();
        while (!glfwWindowShouldClose(GUI::_window)) {
            if (!GUI::isRunning) glfwSetWindowShouldClose(GUI::_window, GL_TRUE);
            if (GUI::renderIsRequested){
                GUI::renderIsRequestedMutex.lock();
                GUI::renderIsRequested = false;
                GUI::renderIsRequestedMutex.unlock();
                GUI::render();
            }
            glfwPollEvents();
        }
        
        // Cleanup everything
        GUI::isRunning = false;
        delete &GUI::_shader;
        GL::deleteTextures(GUI::_textures);
        GUI::clickedSquareSignal.set();
        glfwTerminate();
    }

    void requestRender(){
        GUI::renderIsRequestedMutex.lock();
        GUI::renderIsRequested = true;
        GUI::renderIsRequestedMutex.unlock();
    }

    void init(Board* _board, std::shared_mutex* _boardMutex, Definitions::Theatric* _theatrics){
        GUI::External::board = _board;
        GUI::External::boardMutex = _boardMutex;
        GUI::External::theatrics = _theatrics;
        GUI::_thread = std::thread(GUI::_run);
    }

    void terminate(){
        GUI::isRunning = false;        
        GUI::_thread.join();
    }
};