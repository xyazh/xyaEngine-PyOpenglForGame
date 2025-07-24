#version 430 core

// 格式标记
const int POS = 1;
const int COL = 2;
const int TEX = 4;
const int NOR = 8;
const int LIT = 16;
const int SIZ = 32;

const int DIS = 0;
const int WID = 1;

// 顶点属性
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec4 aColor;
layout(location = 2) in vec2 aTexCoord;
layout(location = 3) in vec3 aNormal;
layout(location = 4) in vec2 aLightMap;
layout(location = 5) in float aSize;

// Uniforms
uniform int fuc;
uniform int formatType;
uniform mat4 scale;
uniform mat4 rotate;
uniform mat4 translate;
uniform mat4 view;
uniform mat4 projection;

// 输出
out vec4 fragColor;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec2 fragLightMap;
flat out int fragFormatType;

void dis()
{
    vec4 worldPos = vec4(aPos, 1.0);
    if ((formatType & POS) != 0) {
        // 之后要用矩阵变换，把这一行改为:
        worldPos = projection * view * translate * rotate * scale * vec4(aPos, 1.0);
        gl_Position = worldPos;
    } else {
        gl_Position = vec4(0.0);
    }

    fragColor      = ((formatType & COL) != 0) ? aColor : vec4(0.0);
    fragTexCoord   = ((formatType & TEX) != 0) ? aTexCoord : vec2(0.0);
    fragNormal     = ((formatType & NOR) != 0) ? aNormal : vec3(0.0, 0.0, 1.0);
    fragLightMap   = ((formatType & LIT) != 0) ? aLightMap : vec2(1.0);
    fragFormatType = formatType;

    if ((formatType & SIZ) != 0) {
        gl_PointSize = aSize / max(gl_Position.z, 0.001);
    }
}

void wid()
{
    // 用于屏幕空间绘制，例如后处理、GUI 等
    gl_Position    = vec4(aPos, 1.0);  // 通常用于传屏幕坐标
    fragColor      = ((formatType & COL) != 0) ? aColor : vec4(0.0);
    fragTexCoord   = ((formatType & TEX) != 0) ? aTexCoord : vec2(0.0);
    fragFormatType = formatType;
}

void main()
{
    if (fuc == DIS) {
        dis();
    } else if (fuc == WID) {
        wid();
    } else {
        // 未来扩展：其他绘制函数
        gl_Position = vec4(0.0); // 避免未定义行为
    }
}
