from scene_state import SceneState
from game_context import GameContext

class MenuScene(SceneState):
    def __init__(self, context: GameContext) -> None:
        super().__init__(context)

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def shouldTransition(self) -> bool:
        return False