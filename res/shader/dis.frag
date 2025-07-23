#version 430 core

// 格式标记（保持与 CPU 和 VS 一致）
const int POS = 1;
const int COL = 2;
const int TEX = 4;
const int NOR = 8;
const int LIT = 16;
const int SIZ = 32;

const int DIS = 0;
const int WID = 1;

// 输入
in vec4 fragColor;
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec2 fragLightMap;
flat in int fragFormatType;

// Uniforms
uniform int fuc;
uniform sampler2D tex;         // 主纹理
uniform sampler2D lightMap;    // 光照贴图

// 输出颜色
out vec4 outColor;

// 默认颜色
const vec4 defaultColor = vec4(1.0);

vec4 dis()
{
    vec4 color = vec4(1.0);

    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        color *= texture(tex, fragTexCoord);
    }

    if ((fragFormatType & LIT) != 0) {
        color *= texture(lightMap, fragLightMap);
    }

    return color;
}

vec4 wid()
{
    vec4 color = vec4(1.0);

    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        color *= texture(tex, fragTexCoord);
    }

    // 通常屏幕渲染不使用法线/光照，但可选添加

    return color;
}

void main()
{
    if (fuc == DIS) {
        outColor = dis();
    } else if (fuc == WID) {
        outColor = wid();
    } else {
        outColor = vec4(1.0, 0.0, 1.0, 1.0); // 未知渲染模式：高亮粉色
    }
}
