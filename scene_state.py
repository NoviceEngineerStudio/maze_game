import abc
from game_context import GameContext

class SceneState(abc.ABC):
    context: GameContext

    def __init__(self, context: GameContext) -> None:
        super().__init__()

        self.context = context

    @abc.abstractmethod
    def enter(self) -> None:
        pass

    @abc.abstractmethod
    def exit(self) -> None:
        pass

    @abc.abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    @abc.abstractmethod
    def draw(self) -> None:
        pass

    @abc.abstractmethod
    def shouldTransition(self) -> bool:
        pass