import pygame as pg
from time import time
from .input import Input
from dataclasses import dataclass
from .game_context import GameContext
from ..scenes import Scene, MenuScene, FadeScene, GameScene, ConclusionScene

__scene_index: int = 0
__scenes: list[Scene] = []
__context: GameContext | None = None

@dataclass
class ApplicationCreateInfo:
    title: str
    render_canvas_size: tuple[int, int]

def __pollJoystick__(is_red: bool) -> int:
    assert pg.font.get_init()
    assert pg.display.get_init()
    
    default_font_name: str = pg.font.get_default_font()
    default_font: pg.font.FontType = pg.font.Font(default_font_name, 18)
    window_surface: pg.Surface = pg.display.get_surface()

    if is_red:
        window_surface.fill((255, 0, 0))

        prompt_text: pg.Surface = default_font.render(
            "Press START on joystick RED",
            False,
            (0, 0, 0)
        )

        window_surface.blit(prompt_text, (0, 0))

        pg.display.flip()
    else:
        window_surface.fill((0, 0, 255))

        prompt_text: pg.Surface = default_font.render(
            "Press START on joystick BLUE",
            False,
            (0, 0, 0)
        )

        window_surface.blit(prompt_text, (0, 0))

        pg.display.flip()

    while True:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    raise SystemExit
                case pg.JOYBUTTONUP:
                    if event.dict["button"] == Input.START_BUTTON:
                        return event.dict["joy"]
                case pg.JOYDEVICEADDED:
                    id: int = event.dict["device_index"]
                    joystick: pg.joystick.JoystickType = pg.joystick.Joystick(id)
                    joystick.init()
                case _:
                    pass

def init(create_info: ApplicationCreateInfo) -> None:
    global __context, __scene_index, __scenes

    print("Initializing Application")

    # ? Initialize Pygame Modules
    pg.init()
    pg.font.init()
    pg.display.init()
    pg.joystick.init()

    # ? Get the Monitor's Size
    monitor_sizes: list[tuple[int, int]] = pg.display.get_desktop_sizes()
    assert len(monitor_sizes) > 0

    # ? Create Application Global State
    __context = GameContext(
        pg.display.set_mode(monitor_sizes[0], pg.FULLSCREEN | pg.SCALED, display=0),
        pg.Surface(create_info.render_canvas_size),
        pg.joystick.Joystick(__pollJoystick__(True)),
        pg.joystick.Joystick(__pollJoystick__(False))
    )

    # ? Initialize Joysticks
    __context.red_joystick.init()
    __context.blue_joystick.init()

    # ? Create Game Scenes
    menu_scene = MenuScene(__context)
    fade_scene = FadeScene(__context)
    conclusion_scene = ConclusionScene(__context)
    game_scene = GameScene(__context, conclusion_scene)

    __scenes = [
        menu_scene,
        fade_scene,
        game_scene,
        conclusion_scene,
        fade_scene
    ]

    # ? Set the Window's Title
    pg.display.set_caption(create_info.title)

def run() -> None:
    global __context, __scene_index, __scenes
    assert not __context is None
    assert len(__scenes) > 0
    assert __scene_index < len(__scenes)

    print("Running Application Main Loop")

    # ? Remove the Mouse Cursor
    pg.mouse.set_visible(False)

    # ? Enter the First Scene
    active_scene: Scene = __scenes[__scene_index]
    active_scene.enter()

    # ? Render Surface Resize Variables
    RENDER_WIDTH, RENDER_HEIGHT = __context.render_surface.get_size()
    RENDER_ASPECT: float = RENDER_WIDTH / RENDER_HEIGHT

    canvas_x: int = 0
    canvas_y: int = 0
    canvas_width: int = 0
    canvas_height: int = 0

    # ? Delta Time Initialization
    cur_frame_time: float = 0.0
    delta_time: float = 0.0

    last_frame_time: float = time()

    # ? Main Loop
    is_running: bool = True
    while is_running:
        cur_frame_time = time()
        delta_time = cur_frame_time - last_frame_time
        last_frame_time = cur_frame_time

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    is_running = False
                    return
                case _:
                    pass

        active_scene.update(delta_time)

        __context.window_surface.fill((0, 0, 0))
        __context.render_surface.fill((0, 0, 0))

        active_scene.draw(__context.render_surface)

        window_width, window_height = pg.display.get_window_size()
        window_aspect: float = window_width / window_height

        if window_aspect > RENDER_ASPECT:
            canvas_height = window_height
            canvas_width = int(canvas_height * RENDER_ASPECT)
        else:
            canvas_width = window_width
            canvas_height = int(canvas_width / RENDER_ASPECT)

        canvas_x = (window_width - canvas_width) // 2
        canvas_y = (window_height - canvas_height) // 2

        scaled_canvas: pg.Surface = pg.transform.scale(
            __context.render_surface,
            (canvas_width, canvas_height)
        )

        __context.window_surface.blit(scaled_canvas, (canvas_x, canvas_y))

        pg.display.flip()

        if active_scene.shouldTransition():
            active_scene.exit()

            __scene_index = (__scene_index + 1) % len(__scenes)

            active_scene = __scenes[__scene_index]
            active_scene.enter()

def shutdown() -> None:
    print("Shutting Down Application")

    # ? Shutdown Pygame Modules
    pg.joystick.quit()
    pg.display.quit()
    pg.font.quit()
    pg.quit()