
g++ main.cpp -o main -lmingw32 -lglew32 -lglu32 -lopengl32 -lglfw3 -lkernel32 -lgdi32 -luser32 -lws2_32 -Wl,-u,___mingw_vsnprintf -Wl,--defsym,___ms_vsnprintf=___mingw_vsnprintf

main