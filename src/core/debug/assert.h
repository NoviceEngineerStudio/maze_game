#ifndef RE_SRC_CORE_DEBUG_ASSERT_H
#define RE_SRC_CORE_DEBUG_ASSERT_H

#ifdef RE_ASSERT_ENABLED

    #include <cstdlib>
    #include "logger.h"

    #define re_assert(condition, ...) \
        do { \
            if (!(condition)) { \
                re_logFatal("Assertion Failed: ", __VA_ARGS__); \
                std::exit(EXIT_FAILURE); \
            } \
        } while(0)

#else

    #define re_assert(condition, ...) ((void)0)

#endif

#endif