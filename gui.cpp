#pragma once
#define GLEW_STATIC
#include <GL/glew.h>
#include "mingw.thread.h"
#include "logging.cpp"
#include <GLFW/glfw3.h>
#include <string>

#include "glHelper.cpp"
#include "shaderHelper.cpp"
#include "vendors/stb/stb_image.h"
#include "vendors/glm/glm.hpp"
#include "vendors/glm/gtc/matrix_transform.hpp"
#include "vendors/glm/gtc/type_ptr.hpp"


namespace GUI{
    std::thread _thread;
    bool isRunning = false;

    unsigned int _vbo;
    unsigned int _ibo;
    Shader _shader;

    glm::mat4 mvp;

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

    void _calculateMVP(){
        mvp = glm::ortho(0.0f, ((float)GUI::WindowProperties::size.first), 0.0f, ((float)GUI::WindowProperties::size.second), -1.0f, 1.0f);
    }

    void render(){
        glfwMakeContextCurrent(GUI::_window);
        glClear(GL_COLOR_BUFFER_BIT);
        
        // Since we only use one _vbo and _ibo, we dont need to rebind it every time

        _shader.setUniformMatrix4f("u_mvp", mvp);
        
        for (int i = 0; i < 64; i++){
            _shader.setUniformInt("square", i);
            // Now we need pieces
            GL::drawSquare();
        }

        glfwSwapBuffers(GUI::_window);
    }

    void _windowSizeCallback(GLFWwindow* _window, int width, int height) {
        glViewport(0, 0, width, height);
        GUI::WindowProperties::size.first = width;
        GUI::WindowProperties::size.second = height;
        _calculateMVP();
        GUI::render();
    }

    void _run(){
        GUI::WindowProperties::size.first = GUI::WindowDefaults::size.first;
        GUI::WindowProperties::size.second = GUI::WindowDefaults::size.second;
        GUI::_window = GL::initialize(GUI::WindowDefaults::size, GUI::WindowDefaults::title);

        if (!GUI::_window){return;}
        GUI::isRunning = true;
                
        glfwSetWindowSizeCallback(GUI::_window, GUI::_windowSizeCallback);
        glfwSwapInterval(1); // Limits the fps at refresh rate of system

        _shader.loadProgramByPath(
            GUI::ShaderPaths::vert,
            GUI::ShaderPaths::frag
        );
        _shader.use();
        
        _vbo = GL::createStaticSquareVertexBuffer();
        _ibo = GL::createStaticSquareIndexBuffer();

        _calculateMVP();

        GUI::render();
        while (!glfwWindowShouldClose(GUI::_window)) {
            if (!GUI::isRunning) glfwSetWindowShouldClose(GUI::_window, GL_TRUE);

            glfwPollEvents();
        }
        _shader.del();
        glfwTerminate();
    }

    void init(){
        GUI::_thread = std::thread(GUI::_run);
    }

    void terminate(){
        GUI::isRunning = false;
        GUI::_thread.join();
    }
};