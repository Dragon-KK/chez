#define GLEW_STATIC
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <iostream>
#include <fstream>

void GLAPIENTRY GLErrorMessageCallback(
    GLenum source,
    GLenum type,
    GLuint id,
    GLenum severity,
    GLsizei length,
    const GLchar* message,
    const void* userParam
){
    std::cerr << "GL CALLBACK:" << ( type == GL_DEBUG_TYPE_ERROR ? " ** GL ERROR **" : "" ) << " type = " << type << ", severity = " << severity << ", message = " << message << std::endl;
}


int main(void)
{
    GLFWwindow* window;
    
    /* Initialize the library */
    if (!glfwInit()){
        std::cout << "Could not init glfw!" << std::endl;
        return -1;
    }
    
    /* Create a windowed mode window and its OpenGL context */
    window = glfwCreateWindow(640, 480, "Hello World", NULL, NULL);
    if (!window)
    {
        std::cerr << "Could not create window!" << std::endl;
        glfwTerminate();
        return -1;
    }
    
    /* Make the window's context current */
    glfwMakeContextCurrent(window);

    if (glewInit() != GLEW_OK){
        std::cerr << "Could not init glew!" << std::endl;
        glfwTerminate();
        return -1;
    }
    glEnable(GL_DEBUG_OUTPUT);
    glDebugMessageCallback(GLErrorMessageCallback, nullptr);

    std::cout << glGetString(GL_VERSION) << std::endl;

    glfwSetWindowSizeCallback(window, [](GLFWwindow* window, int width, int height)
    {
        // TODO! Seperate the draw function
        glClear(GL_COLOR_BUFFER_BIT);
        
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);       


        /* Swap front and back buffers */
        glfwSwapBuffers(window);

        /* Poll for and process events */
        glfwPollEvents();
    });

    unsigned int buffer;
    glCreateBuffers(1, &buffer);

    glBindBuffer(GL_ARRAY_BUFFER, buffer);
    glBufferData(GL_ARRAY_BUFFER, 4 * 2 * sizeof(float), new float[8]{
        -0.5f, -0.5f,
        +0.5f, -0.5f,
        +0.5f, +0.5f,
        -0.5f, +0.5f,
    }, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);
    glEnableVertexAttribArray(0);
    
    unsigned int ibo;
    glCreateBuffers(1, &ibo);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * sizeof(unsigned int), new unsigned int[6]{
        0, 1, 2,
        2, 3, 0,
    }, GL_STATIC_DRAW);

    
    unsigned int program = 0;
    glUseProgram(program);


    /* Loop until the user closes the window */
    while (!glfwWindowShouldClose(window))
    {
        /* Render here */
        glClear(GL_COLOR_BUFFER_BIT);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
        glColor4f(1, 1, 0, 0.5);
        glRectf(0.0, 0, 0.5, 0.5);
        


        /* Swap front and back buffers */
        glfwSwapBuffers(window);

        /* Poll for and process events */
        glfwPollEvents();
    }
    
    glDeleteProgram(program);

    glfwTerminate();
    return 0;
}