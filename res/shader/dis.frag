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
const int HDR = 2;
const int PIN = 3;
const int BLM = 4;
const int MIX = 5;

// 输入
in vec4 fragColor;
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec2 fragLightMap;
flat in int fragFormatType;

// Uniforms
uniform vec2 wh;
uniform vec2 win_wh;
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform sampler2D tex3;
uniform sampler2D tex4;
uniform sampler2D tex5;


uniform int fuc;
// 输出颜色
out vec4 outColor;

// 默认颜色
const vec4 defaultColor = vec4(1.0);


vec3 toneMap(vec3 hdrColor) {
    return hdrColor / (hdrColor + vec3(1.0));
}

vec3 toneMapACES(vec3 x) {
    const float a = 2.51;
    const float b = 0.03;
    const float c = 2.43;
    const float d = 0.59;
    const float e = 0.14;
    return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
}


vec4 dis()
{
    vec4 color = vec4(1.0);

    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        color *= texture(tex0, fragTexCoord);
    }

    if ((fragFormatType & LIT) != 0) {
        color *= texture(tex5, fragLightMap);
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
        color *= texture(tex0, fragTexCoord);
    }

    return color;
}

vec4 hdr()
{
    vec4 color = vec4(1.0);

    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        color *= texture(tex0, fragTexCoord);
    }

    float brightness = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
    if (brightness < 1.0) {
        return vec4(0.0, 0.0, 0.0, 1.0); // 舍弃非高亮区域
    }

    vec3 mapped = toneMapACES(color.rgb);
    return vec4(mapped, 1.0);
}


vec4 pin()
{
    vec4 color = vec4(1.0);
    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }
    if ((fragFormatType & TEX) != 0) {
        vec2 pixTex = fragTexCoord * win_wh;
        vec2 offsets[5] = vec2[](
            vec2(0.0, 0.0),
            vec2(5.0, 5.0),
            vec2(-5.0, 5.0),
            vec2(5.0, -5.0),
            vec2(-5.0, -5.0)
        );
        vec3 sum = vec3(0.0);
        for (int i = 0; i < 5; ++i) {
            vec2 uv = (pixTex + offsets[i]) / win_wh;
            sum += texture(tex0, uv).rgb;
        }

        vec3 avg = sum / 5.0;
        color *= vec4(avg, 1.0);
    }
    return color;
}

vec4 blm()
{
    vec4 color = vec4(1.0);

    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        vec4 hdrColor = texture(tex0, fragTexCoord);
        vec3 mapped = toneMap(hdrColor.rgb);
        color *= vec4(mapped, 1.0);
    }

    return color;
}


vec4 mix()
{
    vec4 color = vec4(1.0);

    if ((fragFormatType & COL) != 0) {
        color *= fragColor;
    }

    if ((fragFormatType & TEX) != 0) {
        vec3 base = texture(tex0, fragTexCoord).rgb;  // 原始图像
        vec3 bloom = texture(tex1, fragTexCoord).rgb; // 模糊后的高亮图
        vec3 combined = base + bloom; // 简单相加

        vec3 mapped = toneMapACES(combined);
        color *= vec4(mapped, 1.0);
    }

    return color;
}


void main()
{
    if (fuc == DIS) {
        outColor = dis();
    } else if (fuc == WID) {
        outColor = wid();
    } else if (fuc == HDR) {
        outColor = hdr();
    } else if (fuc == PIN) {
        outColor = pin();
    } else if (fuc == BLM) {
        outColor = blm();
    } else if (fuc == MIX) {
        outColor = mix();
    } else {
        outColor = vec4(1.0, 0.0, 1.0, 1.0); // 未知渲染模式：高亮粉色
    }
    //outColor = vec4(1.0, 0.0, 1.0, 1.0);
}
