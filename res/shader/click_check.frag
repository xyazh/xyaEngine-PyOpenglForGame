#version 330 core

const int POS = 1;
const int COL = 2;
const int TEX = 4;
const int NOR = 8;
const int LIT = 16;

in vec4 fragColor;
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec2 fragLightMap;

uniform vec4 data_color;

out vec4 FragColor;


void main()
{
    vec4 color = data_color;
    FragColor = color;
}
