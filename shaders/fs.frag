#version 330 core

layout(location=0) out vec4 color;

in vec4 square_color;
in vec4 tex_coord;
uniform sampler2D tex;
void main(){
   vec4 texC = texture2D(tex, tex_coord.xy);   
   color = mix(square_color, texC, texC.a);
}