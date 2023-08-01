#ifdef _WIN32
    #include "mingw.mutex.h"
    #include "mingw.condition_variable.h"
#else
    #include <mutex>
    #include <condition_variable>
#endif



class Signal{

private:
    mutex m;
    condition_variable cv;

public:
    bool isSet = false;
    void wait(){
        // Will block the current thread until the signal is set
        if (isSet){return;}
        unique_lock<mutex> lk(m);
        cv.wait(lk, [this]{return isSet;});
        lk.unlock();
    }

    void set(){
        // Sets the signal
        isSet = true;
        cv.notify_all();
    }

    void reset(){
        // Resets the signal
        isSet = false;
    }
};