from pygame import Surface
from ..core import GameContext
from abc import ABC, abstractmethod

class Scene(ABC):
    def __init__(self, app: GameContext) -> None:
        super().__init__()

        self.app: GameContext = app

    @abstractmethod
    def enter(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    @abstractmethod
    def draw(self, canvas: Surface) -> None:
        pass

    @abstractmethod
    def shouldTransition(self) -> bool:
        pass