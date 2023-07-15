g++ -c main.cpp
g++ main.o -o main -lmingw32 -lglew32 -lglu32 -lopengl32 -lglfw3 -lkernel32 -lgdi32 -luser32 -lws2_32 -Wl,-u,___mingw_vsnprintf -Wl,--defsym,___ms_vsnprintf=___mingw_vsnprintf

@REM g++ main.cpp -Llib -lglew32s -lglu32 -lopengl32 -lglfw3 -lkernel32 -luser32 -lgdi32 -lws2_32 -Wl,-u,___mingw_vsnprintf -Wl,--defsym,___ms_vsnprintf=___mingw_vsnprintf -o main.exe