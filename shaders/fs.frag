#version 330 core

layout(location=0) out vec4 color;

in vec4 s_color;
in vec4 pos;
uniform sampler2D u_Tex;
void main(){
   vec4 texC = texture2D(u_Tex, pos.xy);   
   color = mix(s_color, texC, texC.a);
}