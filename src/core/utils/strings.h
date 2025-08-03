#ifndef RE_SRC_CORE_UTILS_STRINGS_H
#define RE_SRC_CORE_UTILS_STRINGS_H

#include "../types/integers.h"

namespace re {
    /// @brief Get the length of a c-style string.
    /// @param in_str A c-style string.
    /// @return The length of the string, not including the null-terminator.
    constexpr u32 getStrLen(const char* in_str) {
        if (in_str == nullptr) {
            return 0;
        }

        u32 length = 0;
        while (*in_str++ != '\0') {
            ++length;
        }

        return length;
    }

    /// @brief Determine if two c-style strings are equivalent.
    /// @param str_a A c-style string.
    /// @param str_b A c-style string.
    /// @return A boolean indicating if the contents of the strings match.
    constexpr bool isStrEqual(const char* str_a, const char* str_b) {
        if (str_a == str_b) {
            return true;
        }

        if (str_a == nullptr || str_b == nullptr) {
            return false;
        }

        while (*str_a != '\0' && *str_b != '\0') {
            if (*str_a != *str_b) {
                return false;
            }

            ++str_a;
            ++str_b;
        }

        return *str_a == *str_b;
    }
}

#endif