#pragma once
#define STB_IMAGE_IMPLEMENTATION 
#include "vendors/stb/stb_image.h"
#include <string>
#include <GLFW/glfw3.h>
#include <GL/glew.h>
#define RGBA_CHANNEL_SIZE 4
#include "logging.cpp"

class Texture{
public:
    unsigned int id;
    int width;
    int height;
    int bpp;
    Texture(std::string path){
        stbi_set_flip_vertically_on_load(1);
        unsigned char* localBuffer = stbi_load(path.c_str(), &width, &height, &bpp, RGBA_CHANNEL_SIZE);
        glGenTextures(1, &id);
        glBindTexture(GL_TEXTURE_2D, id);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, localBuffer);
        glBindTexture(GL_TEXTURE_2D, 0);
        
        if (localBuffer){
            stbi_image_free(localBuffer);
        }
        else{
            Logger::log("wtf");
        }        
    }
    ~Texture(){
        glDeleteTextures(1, &id);
    }

    void bind(unsigned int slot = 0){
        glActiveTexture(GL_TEXTURE0 + slot);
        glBindTexture(GL_TEXTURE_2D, id);
    }
};