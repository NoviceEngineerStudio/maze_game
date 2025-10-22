import pygame as pg
from enum import IntEnum
from .scene import Scene
from os.path import exists
from .shared_config import UI_RED_TEXT, UI_BLUE_TEXT
from ..core import GameContext, Input, createFont

HIGHSCORE_FILE_PATH: str = "./highscore.txt"

CONCLUSION_PAUSE_TIME: float = 5.0
CONCLUSION_UI_BUFFER_Y: int = 64

class WinStates(IntEnum):
    RED_VICTORY = 0
    BLUE_VICTORY = 1
    DRAW = 2

class ConclusionScene(Scene):
    def __init__(self, app: GameContext) -> None:
        super().__init__(app)

        self.pause_time: float = 0.0

        self.win_state: WinStates = WinStates.DRAW
        self.win_score: int = 0

        self.new_highscore: bool = False
        self.highscore: int = 0

        self.background_image: pg.Surface = pg.Surface((1, 1))

        self.small_font = createFont(64)
        self.large_font = createFont(128)

        self.win_state_text: pg.Surface = pg.Surface((1, 1))
        self.score_text: pg.Surface = pg.Surface((1, 1))
        
        self.new_highscore_text: pg.Surface = self.small_font.render("NEW HIGHSCORE!", False, (255, 255, 255))

        if exists(HIGHSCORE_FILE_PATH):
            with open(HIGHSCORE_FILE_PATH, "r") as highscore_file:
                self.highscore = int(highscore_file.readline())

    def enter(self) -> None:
        self.pause_time = 0.0

        self.background_image = self.app.render_surface.copy()
        self.background_image.fill((50, 50, 50), special_flags=pg.BLEND_RGB_MULT)

        if self.win_score > self.highscore:
            with open(HIGHSCORE_FILE_PATH, "w") as highscore_file:
                highscore_file.write(f"{self.win_score}")

            self.highscore = self.win_score
            self.new_highscore = True

        match self.win_state:
            case WinStates.RED_VICTORY:
                self.win_state_text = self.large_font.render("Red Wins!", False, UI_RED_TEXT)
            case WinStates.BLUE_VICTORY:
                self.win_state_text = self.large_font.render("Blue Wins!", False, UI_BLUE_TEXT)
            case WinStates.DRAW:
                self.win_state_text = self.large_font.render("Draw!", False, (255, 255, 255))

        self.score_text = self.small_font.render(
            f"Highscore: {self.highscore}    |    Score: {self.win_score}",
            False,
            (255, 255, 255)
        )

    def exit(self) -> None:
        self.new_highscore = False

    def update(self, delta_time: float) -> None:
        self.pause_time += delta_time

    def draw(self, canvas: pg.Surface) -> None:
        canvas.blit(self.background_image, (0, 0))

        canvas_width, canvas_height = canvas.get_size()
        win_state_width = self.win_state_text.get_width()
        score_width, score_height = self.score_text.get_size()

        canvas.blit(
            self.win_state_text,
            ((canvas_width - win_state_width) // 2, CONCLUSION_UI_BUFFER_Y)
        )

        canvas.blit(
            self.score_text,
            ((canvas_width - score_width) // 2, canvas_height - score_height - CONCLUSION_UI_BUFFER_Y)
        )

        if self.new_highscore:
            new_highscore_width, new_highscore_height = self.new_highscore_text.get_size()

            canvas.blit(
                self.new_highscore_text,
                ((canvas_width - new_highscore_width) // 2, (canvas_height - new_highscore_height) // 2)
            )

    def shouldTransition(self) -> bool:
        return (
            self.app.red_joystick.get_button(Input.START_BUTTON) or
            self.app.blue_joystick.get_button(Input.START_BUTTON) or
            self.pause_time >= CONCLUSION_PAUSE_TIME
        )
    
    def setFinalScores(self, red_score: int, blue_score: int) -> None:
        if red_score > blue_score:
            self.win_state = WinStates.RED_VICTORY
            self.win_score = red_score
        elif red_score < blue_score:
            self.win_state = WinStates.BLUE_VICTORY
            self.win_score = blue_score
        else:
            self.win_state = WinStates.DRAW
            self.win_score = red_score