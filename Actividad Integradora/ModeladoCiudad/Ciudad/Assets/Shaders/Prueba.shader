Shader "Arturo/Prueba"
{
    Properties
    {
        _MainColor("Main Color", Color) = (1, 1, 1, 1)
    }

    SubShader
    {
        Tags {"RenderType" = "Opaque"}

        Pass
        {
            Name "SMAGC-Unlit"

            HLSLPROGRAM

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            #pragma vertex UnlitVertexShader
            #pragma fragment FragmentShader

            float4 _MainColor;

            struct Attributes
            {
                float4 positionOS : POSITION;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
            };

            Varyings UnlitVertexShader(Attributes input)
            {
                Varyings output = (Varyings)0;
                float4x4 mvp = mul(UNITY_MATRIX_P, mul(UNITY_MATRIX_V, UNITY_MATRIX_M));
                output.positionCS = mul(mvp, input.positionOS);
                return output;
            }

            float4 FragmentShader(Varyings input) : SV_Target
            {
                return _MainColor;
            }

            ENDHLSL
        }
    }
}

