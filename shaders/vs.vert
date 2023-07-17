#version 330 core
#define SQUARE_SIZE 70

layout(location=0) in vec4 position;
uniform mat4 mvp;
uniform int square;
uniform int theatric;

out vec4 square_color;
out vec4 tex_coord;
vec4 bottomLeft = vec4(80, -SQUARE_SIZE * 4, 0, 0);
void main(){
	int mod_8 = square%8;
	int div_8 = 7 - (square/8);
	
	// out position
	gl_Position = (mvp * (position + vec4((mod_8) * SQUARE_SIZE, (div_8) * SQUARE_SIZE, 0, 0) + bottomLeft)) + vec4(0, 1, 0, 0);
	
	// out pos
	tex_coord = position / SQUARE_SIZE;
	// out color
		
	if (theatric == 0){ // none
		square_color = ((div_8%2)^(mod_8%2)) == 0? 
		vec4(1, 0, 0, 1) : vec4(0, 1, 0, 1);
	}
	else if (theatric == 1){ // highlight
		square_color = ((div_8%2)^(mod_8%2)) == 0? 
		vec4(1, 1, 0, 1) : vec4(0, 1, 1, 1);
	}
	else if (theatric == 2){ // marked
		square_color = ((div_8%2)^(mod_8%2)) == 0? 
		vec4(1, 0.5, 0, 1) : vec4(0, 0.5, 1, 1);
	}
	else if (theatric == 3){ // target
		square_color = ((div_8%2)^(mod_8%2)) == 0? 
		vec4(1, 1, 1, 1) : vec4(0, 0, 0, 1);
	}
	


}