#ifndef RE_SRC_CORE_TYPES_FLOATS_H
#define RE_SRC_CORE_TYPES_FLOATS_H

#include "../base.h"

namespace re {
    typedef float f32;

    static_assert(sizeof(f32) == 4, "Size of f32 is not 4 bytes!");

    constexpr f32 MIN_POS_F32 = 1.175494351e-38f;
    constexpr f32 MAX_F32 = 3.402823466e+38F;
    constexpr f32 MIN_F32 = -MAX_F32;

#ifdef RE_X64
    typedef double f64;

    static_assert(sizeof(f64) == 8, "Size of f64 is not 8 bytes!");

    constexpr f64 MIN_POS_F64 = 2.2250738585072014e-308;
    constexpr f64 MAX_F64 = 1.7976931348623158e+308;
    constexpr f64 MIN_F64 = -MAX_F64;
#endif
}

#endif