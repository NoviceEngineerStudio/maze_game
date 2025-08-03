#include "../main.h"

#include <raylib.h>

struct re::Application_T {
    bool is_running = false;
};

re::Application re::createApplication(const re::CommandLineArguments& args) {
    re::Application app = new re::Application_T();

    app->is_running = false;

    InitWindow(800, 450, "Maze Game");

    return app;
}

void re::destroyApplication(re::Application app) {
    CloseWindow();
}

void re::runApplication(re::Application app) {
    bool& is_running = app->is_running;

    is_running = true;
    while (is_running) {
        BeginDrawing();
        ClearBackground(BLACK);

        EndDrawing();

        is_running &= !WindowShouldClose();
    }
}