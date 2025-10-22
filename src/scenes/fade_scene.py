import pygame as pg
from .scene import Scene
from ..core import GameContext

FADE_ANIMATION_TIME: float = 1.0
FADE_PAUSE_TIME: float = 0.25

class FadeScene(Scene):
    def __init__(self, app: GameContext) -> None:
        super().__init__(app)

        self.fade_time: float = 0.0
        self.background_image: pg.Surface = pg.Surface((1, 1))

    def enter(self) -> None:
        self.fade_time = 0.0
        self.background_image = self.app.render_surface.copy()

    def exit(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.fade_time += delta_time

    def draw(self, canvas: pg.Surface) -> None:
        global FADE_ANIMATION_TIME
        
        canvas_width, canvas_height = canvas.get_size()

        canvas.blit(self.background_image, (0, 0))

        t: float = min(1.0, self.fade_time / FADE_ANIMATION_TIME)
        pg.draw.rect(
            canvas,
            (0, 0, 0),
            (0, 0, canvas_width, int(canvas_height * t))
        )

    def shouldTransition(self) -> bool:
        global FADE_PAUSE_TIME, FADE_ANIMATION_TIME

        return 1.0 <= (self.fade_time / (FADE_ANIMATION_TIME + FADE_PAUSE_TIME))