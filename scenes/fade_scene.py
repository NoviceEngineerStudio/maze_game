import pygame as pg
from scene_state import SceneState
from game_context import GameContext

FADE_ANIMATION_TIME: float = 1.0
TRANSITION_PAUSE_TIME: float = 0.25

class FadeScene(SceneState):
    fade_step: float = 0.0

    def __init__(self, context: GameContext) -> None:
        super().__init__(context)

    def enter(self) -> None:
        self.fade_step = 0.0

    def exit(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.fade_step += delta_time

    def draw(self) -> None:
        t: float = min(1.0, self.fade_step / FADE_ANIMATION_TIME)

        pg.draw.rect(
            self.context.canvas,
            (0, 0, 0),
            (0, 0, self.context.canvas_width, int(t * self.context.canvas_height))
        )

    def shouldTransition(self) -> bool:
        return 1.0 <= (self.fade_step / (FADE_ANIMATION_TIME + TRANSITION_PAUSE_TIME))