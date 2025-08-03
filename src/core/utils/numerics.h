#ifndef RE_SCR_CORE_UTILS_NUMERICS_H
#define RE_SCR_CORE_UTILS_NUMERICS_H

#define __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(Type) \
    constexpr Type min(const Type val_a, const Type val_b) { \
        return (val_a < val_b) ? val_a : val_b; \
    } \
    constexpr Type max(const Type val_a, const Type val_b) { \
        return (val_a > val_b) ? val_a : val_b; \
    } \
    constexpr Type clamp(const Type value, const Type lower_bound, const Type upper_bound) { \
        if (value >= upper_bound) { \
            return upper_bound; \
        } \
        return (value > lower_bound) ? value : lower_bound; \
    }

#define __RE_DEFINE_2_BYTES_TO_TYPE_METHOD__(Type) \
    constexpr Type Type##From2Bytes( \
        const char b0, \
        const char b1 = char(0x00) \
    ) { \
        return static_cast<Type>( \
            static_cast<Type>(b0) | \
            (static_cast<Type>(b1) << 8) \
        );\
    }

#define __RE_DEFINE_4_BYTES_TO_TYPE_METHOD__(Type) \
    constexpr Type Type##From4Bytes( \
        const char b0, \
        const char b1 = char(0x00), \
        const char b2 = char(0x00), \
        const char b3 = char(0x00) \
    ) { \
        return static_cast<Type>( \
            static_cast<Type>(b0) | \
            (static_cast<Type>(b1) << 8) | \
            (static_cast<Type>(b2) << 16) | \
            (static_cast<Type>(b3) << 24) \
        );\
    }

#define __RE_DEFINE_8_BYTES_TO_TYPE_METHOD__(Type) \
    constexpr Type Type##From8Bytes( \
        const char b0, \
        const char b1 = char(0x00), \
        const char b2 = char(0x00), \
        const char b3 = char(0x00), \
        const char b4 = char(0x00), \
        const char b5 = char(0x00), \
        const char b6 = char(0x00), \
        const char b7 = char(0x00) \
    ) { \
        return static_cast<Type>( \
            static_cast<Type>(b0) | \
            (static_cast<Type>(b1) << 8) | \
            (static_cast<Type>(b2) << 16) | \
            (static_cast<Type>(b3) << 24) | \
            (static_cast<Type>(b4) << 32) | \
            (static_cast<Type>(b5) << 40) | \
            (static_cast<Type>(b6) << 48) | \
            (static_cast<Type>(b7) << 56) \
        );\
    }

#include "../base.h"
#include "../types/floats.h"
#include "../types/integers.h"

namespace re {
    // *=================================================
    // *
    // * Min, Max, and Clamp Methods
    // *
    // *=================================================

    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(i8);
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(i16);
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(i32);

    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(u8);
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(u16);
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(u32);

    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(f32);

#ifdef RE_X64
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(i64);
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(u64);
    __RE_DEFINE_NUMERIC_COMPARISON_METHODS__(f64);
#endif

    // *=================================================
    // *
    // * Byte List to Type Conversion Methods
    // *
    // *=================================================

    __RE_DEFINE_2_BYTES_TO_TYPE_METHOD__(i16);
    __RE_DEFINE_2_BYTES_TO_TYPE_METHOD__(u16);

    __RE_DEFINE_4_BYTES_TO_TYPE_METHOD__(i32);
    __RE_DEFINE_4_BYTES_TO_TYPE_METHOD__(u32);

#ifdef RE_X64
    __RE_DEFINE_8_BYTES_TO_TYPE_METHOD__(i64);
    __RE_DEFINE_8_BYTES_TO_TYPE_METHOD__(u64);
#endif
}

#endif