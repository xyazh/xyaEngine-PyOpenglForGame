#version 330 core

const int POS = 1;      // 位置
const int COL = 2;      // 颜色
const int TEX = 4;      // UV
const int NOR = 8;      // 法线
const int LIT = 16;     // 光照贴图
const int SIZ = 32;     // 点尺寸

layout(location = 0) in vec3 aPos;       // 位置
layout(location = 1) in vec4 aColor;     // 颜色
layout(location = 2) in vec2 aTexCoord;  // UV
layout(location = 3) in vec3 aNormal;    // 法线
layout(location = 4) in vec2 aLightMap;  // 光照贴图
layout(location = 5) in float aSize;     // 点尺寸

uniform int formatType;  // 控制布局的类型

out vec4 fragColor;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec2 fragLightMap;
flat out int fragFormatType;

void main()
{
    // 默认值
    fragColor = vec4(0.0);
    fragTexCoord = vec2(0.0);
    fragNormal = vec3(0.0, 0.0, 1.0);
    fragLightMap = vec2(1.0);
    fragFormatType = formatType;

    // 根据 formatType 选择性启用属性
    if ((formatType & POS) != 0) {
        gl_Position = vec4(aPos, 1.0);
    }

    if ((formatType & COL) != 0) {
        fragColor = aColor;
    }

    if ((formatType & TEX) != 0) {
        fragTexCoord = aTexCoord;
    }

    if ((formatType & NOR) != 0) {
        fragNormal = aNormal;
    }

    if ((formatType & LIT) != 0) {
        fragLightMap = aLightMap;
    }
}
