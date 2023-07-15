#version 330 core
#define SQUARE_SIZE 70

layout(location=0) in vec4 position;
uniform mat4 u_mvp;
uniform int square;

out vec4 s_color;

vec4 bottomLeft = vec4(80, -SQUARE_SIZE * 4, 0, 0);
void main(){
   int mod_8 = square%8;
   int div_8 = square/8;
   
   // out position
   gl_Position = (u_mvp * (position + vec4((mod_8) * SQUARE_SIZE, (div_8) * SQUARE_SIZE, 0, 0) + bottomLeft)) + vec4(0, 1, 0, 0);
   
   // out color
   s_color = ((div_8%2)^(mod_8%2)) == 0? 
         vec4(1, 0, 0, 1) : vec4(0, 1, 0, 1);
}