#include <raylib.h>

int main(void) {
    InitWindow(800, 450, "Maze Game");

    while (!WindowShouldClose()) {
        BeginDrawing();
        
        ClearBackground(BLACK);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}