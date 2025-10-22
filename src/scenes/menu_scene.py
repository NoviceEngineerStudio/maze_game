import pygame as pg
from .scene import Scene
from ..core import Input, createFont, GameContext

PRESS_START_PROMPT: str = "Press Start"

class MenuScene(Scene):
    def __init__(self, app: GameContext) -> None:
        global PRESS_START_PROMPT

        super().__init__(app)

        self.prompt_font = createFont(48)

        self.last_canvas_width: int = 0
        self.last_canvas_height: int = 0

        self.prompt_texture: pg.Surface = self.prompt_font.render(
            PRESS_START_PROMPT,
            False,
            (255, 255, 255)
        )

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, canvas: pg.Surface) -> None:
        canvas_width, canvas_height = canvas.get_size()
        prompt_width, prompt_height = self.prompt_texture.get_size()

        canvas.blit(self.prompt_texture, ((canvas_width - prompt_width) // 2, (canvas_height - prompt_height) // 2))

    def shouldTransition(self) -> bool:
        return (
            self.app.red_joystick.get_button(Input.START_BUTTON) or
            self.app.blue_joystick.get_button(Input.START_BUTTON)
        )