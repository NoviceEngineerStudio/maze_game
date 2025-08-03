#ifndef RE_SRC_CORE_BASE_H
#define RE_SRC_CORE_BASE_H

// *=================================================
// *
// * Base Constants
// *
// *=================================================

// Numbering convention is XAA
// X - Platform Type ID
// AA - Platform Specific ID

// Desktop Platforms

#define RE_PL_WINDOWS 000
#define RE_PL_LINUX 001
#define RE_PL_MACOS 002

// Mobile Platforms

#define RE_PL_IOS 100
#define RE_PL_ANDROID 101

// Embedded Platforms

#define RE_PL_RASPBERRY_PI 200

// *=================================================
// *
// * Target Build Platform
// *
// *=================================================

#if defined(_WIN32) || defined(_WIN64)
    #define RE_PLATFORM RE_PL_WINDOWS
#elif defined(__linux__)
    #define RE_PLATFORM RE_PL_LINUX
#elif defined(__APPLE__) || defined(__MACH__)
    #if defined(TARGET_OS_IPHONE)
        #define RE_PLATFORM RE_PL_IOS
    #elif defined(TARGET_OS_MAC)
        #define RE_PLATFORM RE_PL_MACOS
    #else
        #error "Attempting to compile for unknown Apple platform!"
    #endif
#elif defined(__ANDROID__)
    #define RE_PLATFORM RE_PL_ANDROID
#elif defined(__arm__)
    #define RE_PLATFORM RE_PL_RASPBERRY_PI
#else
    #error "Attempting to compile for unknown platform!"
#endif

// *=================================================
// *
// * 64-Bit Support
// *
// *=================================================

#if defined(_M_X64) || defined(__x86_64__) || defined(__amd64__) || \
    defined(__aarch64__) || defined(_M_ARM64) || defined(__ppc64__)
    #define RE_X64 1
#endif

#endif