#include "application.h"

#include "../core.h"

#define __RE_DEFINE_ENTRY_POINT__(__cmd_argc, __cmd_argv) \
    do { \
        re_logInfo("Initializing Application..."); \
        const re::CommandLineArguments __cmd_args = { \
            .arguments = __cmd_argv, \
            .count = static_cast<re::u32>(__cmd_argc), \
        }; \
        re::Application __app = re::createApplication(__cmd_args); \
        re_logInfo("Entering Application Main Loop..."); \
        re::runApplication(__app); \
        re_logInfo("Shutting Down Application..."); \
        re::destroyApplication(__app); \
        delete __app; \
        re_logSuccess("Successfully Exited Application!"); \
    } while(0)

#if RE_PLATFORM == RE_PL_WINDOWS && defined(RE_GUI_BUILD)

    #include <Windows.h>

    int WINAPI WinMain(
        HINSTANCE hInstance,
        HINSTANCE hPrevInstance,
        LPSTR lpCmdLine,
        int nCmdShow
    ) {
        int argcW = 0;
        LPWSTR* argvW = CommandLineToArgvW(GetCommandLineW(), &argcW);

        if (argvW == nullptr) {
            __RE_DEFINE_ENTRY_POINT__(0, nullptr);
            return 0;
        }

        const int argc = argcW;
        char** argv = new char*[argc];

        for (re::u32 idx = 0; idx < argc; ++idx) {
            LPWSTR& cmd_argW = argvW[idx];
            char*& cmd_arg = argv[idx];

            int length = WideCharToMultiByte(
                CP_UTF8,
                0,
                cmd_argW,
                -1,
                nullptr,
                0,
                nullptr,
                nullptr
            );

            cmd_arg = new char[length];
            WideCharToMultiByte(
                CP_UTF8,
                0,
                cmd_argW,
                -1,
                cmd_arg,
                length,
                nullptr,
                nullptr
            );
        }

        LocalFree(argvW);

        __RE_DEFINE_ENTRY_POINT__(argc, argv);

        for (re::u32 idx = 0; idx < argc; ++idx) {
            delete[] argv[idx];
        }

        delete[] argv;

        return 0;
    }

#elif ( \
    RE_PLATFORM == RE_PL_LINUX || \
    RE_PLATFORM == RE_PL_MACOS || \
    RE_PLATFORM == RE_PL_RASPBERRY_PI ||\
    (RE_PLATFORM == RE_PL_WINDOWS && !defined(RE_GUI_BUILD)) \
)

    int main(int argc, char** argv) {
        __RE_DEFINE_ENTRY_POINT__(argc, argv);
        return 0;
    }

#else

    #error "Platform entry point is undefined!"

#endif