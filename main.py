import time as tm
import pygame as pg
from scene_state import SceneState
from game_context import GameContext
from scenes import MenuScene, FadeScene, GameScene, ConclusionScene

if __name__ != "__main__":
    quit(1)

pg.init()

CANVAS_WIDTH: int = 1280
CANVAS_HEIGHT: int = 720

context: GameContext = GameContext(
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
)

scenes: list[SceneState] = [
    MenuScene(context),
    FadeScene(context),
    GameScene(context),
    ConclusionScene(context),
    FadeScene(context)
]

scene_index: int = 0
active_scene: SceneState = scenes[scene_index]
active_scene.enter()

screen_width: int = 1280
screen_height: int = 720

screen: pg.Surface = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Maze Game")
# pg.display.toggle_fullscreen()

canvas_x: int = 0
canvas_y: int = 0
canvas_w: int = 0
canvas_h: int = 0

delta_time: float = 0.0
cur_frame_time: float = 0.0
last_frame_time: float = tm.time()

is_running: bool = True
while is_running:
    cur_frame_time = tm.time()
    delta_time = cur_frame_time - last_frame_time
    last_frame_time = cur_frame_time

    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                is_running = False
                break
            case _:
                pass

    active_scene.update(delta_time)

    screen.fill((0, 0, 0))
    context.canvas.fill((0, 50, 0))

    active_scene.draw()
    
    screen_width, screen_height = pg.display.get_window_size()
    if abs(screen_width - CANVAS_WIDTH) < abs(screen_height - CANVAS_HEIGHT):
        canvas_w = screen_width
        canvas_h = canvas_w * CANVAS_HEIGHT // CANVAS_WIDTH
    else:
        canvas_h = screen_height
        canvas_w = canvas_h * CANVAS_WIDTH // CANVAS_HEIGHT

    canvas_x = (screen_width - canvas_w) >> 1
    canvas_y = (screen_height - canvas_h) >> 1

    screen.blit(context.canvas, (canvas_x, canvas_y, canvas_w, canvas_h))
    pg.display.flip()

    if active_scene.shouldTransition():
        active_scene.exit()

        scene_index = (scene_index + 1) % len(scenes)
        active_scene = scenes[scene_index]
        active_scene.enter()

pg.quit()