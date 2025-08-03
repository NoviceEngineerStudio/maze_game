#ifndef RE_SRC_MAIN_APPLICATION_H
#define RE_SRC_MAIN_APPLICATION_H

#include "../core.h"

namespace re {
    struct CommandLineArguments {
        char** arguments = nullptr;
        u32 count = 0;
    };
    
    struct Application_T;
    typedef Application_T* Application;

    Application createApplication(const CommandLineArguments& args);
    void destroyApplication(Application app);

    void runApplication(Application app);
}

#endif