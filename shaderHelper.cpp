#pragma once
#include <string>
#include <fstream>
#include <GL/glew.h>
#include "logging.cpp"
#include <unordered_map>
#include "vendors/glm/glm.hpp"
#include "vendors/glm/gtc/type_ptr.hpp"

class Shader{
private:
    std::unordered_map<string, int> uniformMap;
    static unsigned int compileShader(std::string& src, unsigned int type){
        unsigned int id = glCreateShader(type);
        const char* source = src.c_str();
        glShaderSource(id, 1, &source, nullptr);
        glCompileShader(id);

        int result;
        glGetShaderiv(id, GL_COMPILE_STATUS, &result);
        if (result == GL_FALSE){
            int length;
            glGetShaderiv(id, GL_INFO_LOG_LENGTH, &length);
            char message[length];
            glGetShaderInfoLog(id, length, &length, message);

            Logger::error("Failed to compile shader!");
            Logger::error(message);
            glDeleteShader(id);
            return 0;
        }

        return id;
    }
public:
    unsigned int program = 0;
    void loadProgramBySource(string& vsSrc, string& fsSrc){
        program = glCreateProgram();
        unsigned int vs = compileShader(vsSrc, GL_VERTEX_SHADER);
        unsigned int fs = compileShader(fsSrc, GL_FRAGMENT_SHADER);
        glAttachShader(program, vs);
        glAttachShader(program, fs);

        glLinkProgram(program);
        glValidateProgram(program);

        glDeleteShader(vs);
        glDeleteShader(fs);
    }
    void loadProgramByPath(string& vsPath, string& fsPath){
        std::ifstream vstream(vsPath);
        std::string vstring(
            (std::istreambuf_iterator<char>(vstream)),
            std::istreambuf_iterator<char>()
        );
        std::ifstream fstream(fsPath);
        std::string fstring(
            (std::istreambuf_iterator<char>(fstream)), 
            std::istreambuf_iterator<char>()
        );

        loadProgramBySource(vstring, fstring);
    }
    void setUniformMatrix4f(string name, glm::mat4 matrix){
        auto it = uniformMap.find(name);
        int loc;
        if (it != uniformMap.end()){
            loc = it->second;
        }
        else{
            loc = glGetUniformLocation(program, name.c_str());
            if (loc == -1){
                Logger::error("Could not find uniform of name: `" + name + "` !");
                return;
            }
            uniformMap[name] = loc;
        }
        glUniformMatrix4fv(loc, 1, GL_FALSE, glm::value_ptr(matrix));
    }
    void setUniformInt(string name, int number){
        auto it = uniformMap.find(name);
        int loc;
        if (it != uniformMap.end()){
            loc = it->second;
        }
        else{
            loc = glGetUniformLocation(program, name.c_str());
            if (loc == -1){
                Logger::error("Could not find uniform of name: `" + name + "` !");
                return;
            }
            uniformMap[name] = loc;
        }
        glUniform1i(loc, number);
    }
    void use(){
        glUseProgram(program);
    }
    void del(){
        glDeleteProgram(program);
    }
};