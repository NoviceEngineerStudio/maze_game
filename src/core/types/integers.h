#ifndef RE_SRC_CORE_TYPES_INTEGERS_H
#define RE_SRC_CORE_TYPES_INTEGERS_H

#include "../base.h"

namespace re {
    typedef signed char i8;
    typedef signed short i16;
    typedef signed int i32;

    typedef unsigned char u8;
    typedef unsigned short u16;
    typedef unsigned int u32;

    static_assert(sizeof(i8) == 1, "Size of i8 is not 1 byte!");
    static_assert(sizeof(i16) == 2, "Size of i16 is not 2 bytes!");
    static_assert(sizeof(i32) == 4, "Size of i32 is not 4 bytes!");

    static_assert(sizeof(u8) == 1, "Size of u8 is not 1 byte!");
    static_assert(sizeof(u16) == 2, "Size of u16 is not 2 bytes!");
    static_assert(sizeof(u32) == 4, "Size of u32 is not 4 bytes!");

    constexpr i8 MIN_I8 = i8(0x80);
    constexpr i8 MAX_I8 = i8(0x7F);

    constexpr i16 MIN_I16 = i16(0x8000);
    constexpr i16 MAX_I16 = i16(0x7FFF);

    constexpr i32 MIN_I32 = i32(0x80000000);
    constexpr i32 MAX_I32 = i32(0x7FFFFFFF);

    constexpr u8 MIN_U8 = u8(0x00);
    constexpr u8 MAX_U8 = u8(0xFF);

    constexpr u16 MIN_U16 = u16(0x0000);
    constexpr u16 MAX_U16 = u16(0xFFFF);

    constexpr u32 MIN_U32 = u32(0x00000000);
    constexpr u32 MAX_U32 = u32(0xFFFFFFFF);

#ifdef RE_X64

    typedef signed long long i64;
    typedef unsigned long long u64;

    static_assert(sizeof(i64) == 8, "Size of i64 is not 8 bytes!");
    static_assert(sizeof(u64) == 8, "Size of u64 is not 8 bytes!");

    constexpr i64 MIN_I64 = i64(0x8000000000000000);
    constexpr i64 MAX_I64 = i64(0x7FFFFFFFFFFFFFFF);

    constexpr u64 MIN_U64 = u64(0x0000000000000000);
    constexpr u64 MAX_U64 = u64(0xFFFFFFFFFFFFFFFF);

    typedef u64 size;

    constexpr size MAX_SIZE = MAX_U64;
#else
    typedef u32 size;

    constexpr size MAX_SIZE = MAX_U32;
#endif

    constexpr size MIN_SIZE = 0;
}

#endif