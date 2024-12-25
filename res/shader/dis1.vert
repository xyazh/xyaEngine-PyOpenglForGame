#version 330 core

const int POS = 1;      // 位置
const int COL = 2;      // 颜色
const int TEX = 4;      // UV

layout(location = 0) in vec3 aPos;       // 位置
layout(location = 1) in vec4 aColor;     // 颜色
layout(location = 2) in vec2 aTexCoord;  // UV

uniform int formatType;  // 控制布局的类型

out vec4 fragColor;
out vec2 fragTexCoord;
flat out int fragFormatType;

void main()
{
    fragColor = vec4(0.0);
    fragTexCoord = vec2(0.0);
    fragFormatType = formatType;
    gl_Position = vec4(aPos, 1.0);
    

    if ((formatType & COL) != 0) {
        fragColor = aColor;
    }

    if ((formatType & TEX) != 0) {
        fragTexCoord = aTexCoord;
    }
}
