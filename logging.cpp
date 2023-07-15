#pragma once
#include <iostream>
#include <string>

using namespace std;
namespace Logger{
    void log(string message){
        cout << message << endl;
    }

    void log_int(int i){
        cout << i << endl;
    }

    void error(string message){
        cerr << message << endl;
    }
};