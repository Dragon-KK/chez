#pragma once
#include "imgHelper.cpp"
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "logging.cpp"
#include <string>

#define TEXTURE_COUNT 14
#define SQUARE_SIZE 70

namespace GL{
    GLFWwindow* initialize(pair<int, int> defaultWindowSize, string defaultWindowName){
        if (!glfwInit()){
            Logger::error("Could not initialize glfw!");
            return nullptr;
        }
        GLFWwindow* window = glfwCreateWindow(defaultWindowSize.first, defaultWindowSize.second, defaultWindowName.c_str(), NULL, NULL);

        if (!window){
            Logger::error("Could not create window!");
            glfwTerminate();
            return nullptr;
        }

        glfwMakeContextCurrent(window);

        if (glewInit() != GLEW_OK){
            Logger::error("Could not initialize glew!");
            glfwTerminate();
            return nullptr;
        }

        return window;
    }

    unsigned int createStaticSquareVertexBuffer(){
        unsigned int buff;
        glCreateBuffers(1, &buff);

        glBindBuffer(GL_ARRAY_BUFFER, buff);
        glBufferData(GL_ARRAY_BUFFER, 4 * 2 * sizeof(float), new float[8]{
            SQUARE_SIZE, SQUARE_SIZE,
            00.0f, SQUARE_SIZE,
            00.0f, 00.0f,
            SQUARE_SIZE, 00.0f,
        }, GL_STATIC_DRAW);
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);
        glEnableVertexAttribArray(0);
    }

    unsigned int createStaticSquareIndexBuffer(){
        unsigned int ibo;
        glCreateBuffers(1, &ibo);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * sizeof(unsigned int), new unsigned int[6]{
            0, 1, 2,
            2, 3, 0,
        }, GL_STATIC_DRAW);
        return ibo;
    }

    void drawSquare(){
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
    }

    Texture* createTextures(){
        return new Texture[TEXTURE_COUNT]{
            Texture("assets/na.png", 0 ),
            Texture("assets/na.png", 1 ),
            Texture("assets/bP.png", 2 ),
            Texture("assets/wP.png", 3 ),
            Texture("assets/bN.png", 4 ),
            Texture("assets/wN.png", 5 ),
            Texture("assets/bB.png", 6 ),
            Texture("assets/wB.png", 7 ),
            Texture("assets/bR.png", 8 ),
            Texture("assets/wR.png", 9 ),
            Texture("assets/bQ.png", 10),
            Texture("assets/wQ.png", 11),
            Texture("assets/bK.png", 12),
            Texture("assets/wK.png", 13),            
        };
    }

    void deleteTextures(Texture* texture){
        for (int i=0; i<TEXTURE_COUNT; i++){ delete &texture[i]; }
    }
}