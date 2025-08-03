#ifndef RE_SRC_CORE_DEBUG_LOGGER_H
#define RE_SRC_CORE_DEBUG_LOGGER_H

#ifdef RE_LOGGER_ENABLED

    #include <chrono>
    #include <fstream>
    #include <iostream>

    namespace re {
        static std::fstream __log_file;
        static std::ostream __internal_logger = std::ostream(std::cout.rdbuf());

        template <typename ...Args>
        void __logMsg(const char* log_level, Args&&... args) {
            std::tm tm;
            time_t now = std::chrono::system_clock::to_time_t(
                std::chrono::system_clock::now()
            );

            localtime_s(&tm, &now);

            __internal_logger << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
            __internal_logger << " [" << log_level << "]: ";
            (__internal_logger << ... << args);
            __internal_logger << std::endl;
        }
    }

    #define re_logInfo(...) re::__logMsg("INFO", __VA_ARGS__)
    #define re_logDebug(...) re::__logMsg("DEBUG", __VA_ARGS__)
    #define re_logSuccess(...) re::__logMsg("SUCCESS", __VA_ARGS__)

    #define re_logWarn(...) re::__logMsg("WARN", \
        "(File: ", __FILE__, "; Line: ", __LINE__, ") ", __VA_ARGS__)
    #define re_logError(...) re::__logMsg("ERROR", \
        "(File: ", __FILE__, "; Line: ", __LINE__, ") ", __VA_ARGS__)
    #define re_logFatal(...) re::__logMsg("FATAL", \
        "(File: ", __FILE__, "; Line: ", __LINE__, ") ", __VA_ARGS__)

    #define re_closeLogFile() \
        do { \
            if (re::__log_file.is_open()) { \
                re::__log_file.close(); \
                re::__internal_logger.set_rdbuf(std::cout.rdbuf()) \
            } \
        } while(0)

    #define re_setLogFile(file_path) \
        do { \
            re_closeLogFile(); \
            re::__log_file.open(file_path); \
            if (!re::__log_file.is_open()) {\
                re_logWarn("Failed to open logging file: ", file_path); \
            } \
            else { \
                re::__internal_logger.set_rdbuf(re::__log_file.rdbuf()) \
            } \
        } while(0)

#else

    #define re_setLogFile(file_path) ((void)(0))
    #define re_closeLogFile() ((void)(0))

    #define re_logInfo(...) ((void)0)
    #define re_logDebug(...) ((void)0)
    #define re_logSuccess(...) ((void)0)

    #define re_logWarn(...) ((void)0)
    #define re_logError(...) ((void)0)
    #define re_logFatal(...) ((void)0)

#endif

#endif