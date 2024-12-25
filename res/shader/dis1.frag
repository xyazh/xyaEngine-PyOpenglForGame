#version 330 core

const int POS = 1;
const int COL = 2;
const int TEX = 4;

in vec4 fragColor;
in vec2 fragTexCoord;
flat in int fragFormatType;

out vec4 FragColor;

uniform sampler2D textureSampler;

void main()
{
    vec4 color = vec4(1.0,1.0,1.0,1.0);
    if ((fragFormatType & COL) != 0) {
        color = fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        vec4 texColor = texture(textureSampler, fragTexCoord);
        color = texColor;
    }

    FragColor = color;
}
