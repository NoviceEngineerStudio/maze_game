import pygame as pg
from .scene import Scene
from ..core import GameContext, createFont
from ..entities import Player, MazeManager
from .conclusion_scene import ConclusionScene
from .shared_config import UI_RED_TEXT, UI_BLUE_TEXT

GAME_DURATION: float = 45.0

GAME_UI_BUFFER_X: int = 8
GAME_UI_BUFFER_Y: int = 16

class GameScene(Scene):
    def __init__(self, app: GameContext, conclusion_scene: ConclusionScene) -> None:
        super().__init__(app)

        self.conclusion_scene = conclusion_scene

        self.game_time: float = 0.0

        self.red_player: Player = Player(True, app.red_joystick)
        self.blue_player: Player = Player(False, app.blue_joystick)

        self.maze_manager: MazeManager = MazeManager()

        self.ui_font: pg.font.FontType = createFont(56)

    def enter(self) -> None:
        self.game_time = GAME_DURATION

        self.red_player.reset()
        self.blue_player.reset()

        self.maze_manager.reset()

    def exit(self) -> None:
        self.conclusion_scene.setFinalScores(
            self.red_player.getScore(),
            self.blue_player.getScore()
        )

    def update(self, delta_time: float) -> None:
        self.game_time -= delta_time
        if self.game_time < 0.0:
            self.game_time = 0.0

        self.maze_manager.update(delta_time)

        self.red_player.updateMovement(delta_time)
        self.blue_player.updateMovement(delta_time)

        self.red_player.handleWallCollisions(self.maze_manager.getSolidMask())
        self.blue_player.handleWallCollisions(self.maze_manager.getSolidMask())

    def draw(self, canvas: pg.Surface) -> None:
        canvas_width, canvas_height = canvas.get_size()

        self.maze_manager.drawMaze(canvas)

        self.red_player.draw(canvas)
        self.blue_player.draw(canvas)

        # ? UI Rendering

        red_score_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{self.red_player.getScore()}pts",
            False,
            UI_RED_TEXT
        ), 90.0)

        red_time_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{int(self.game_time)}s",
            False,
            UI_RED_TEXT
        ), 90.0)

        blue_score_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{self.blue_player.getScore()}pts",
            False,
            UI_BLUE_TEXT
        ), 270.0)

        blue_time_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{int(self.game_time)}s",
            False,
            UI_BLUE_TEXT
        ), 270.0)

        red_score_width, red_score_height = red_score_text.get_size()
        red_time_width = red_time_text.get_width()
        blue_time_height = blue_time_text.get_height()

        canvas.blit(
            red_score_text,
            (canvas_width - red_score_width - GAME_UI_BUFFER_X, canvas_height - red_score_height - GAME_UI_BUFFER_Y)
        )

        canvas.blit(
            red_time_text,
            (canvas_width - red_time_width - GAME_UI_BUFFER_X, GAME_UI_BUFFER_Y)
        )

        canvas.blit(
            blue_score_text,
            (GAME_UI_BUFFER_X, GAME_UI_BUFFER_Y)
        )

        canvas.blit(
            blue_time_text,
            (GAME_UI_BUFFER_X, canvas_height - blue_time_height - GAME_UI_BUFFER_Y)
        )

    def shouldTransition(self) -> bool:
        return self.game_time <= 0.0