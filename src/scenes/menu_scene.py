import pygame as pg
from math import sin
from .scene import Scene
from random import random
from ..core import Input, createFont, GameContext, getTexture

PRESS_START_PROMPT: str = "Press Start"

MENU_MONSTER_SPRITE_GAP: int = 128
MENU_MONSTER_SPRITE_BUFFER_Y: int = 64
MENU_MONSTER_SPRITE_SCALE: float = 7.0

MENU_MONSTER_BOB_DELTA: int = 16
MENU_MONSTER_START_TIME_RANGE: float = 1000.0

class MenuScene(Scene):
    def __init__(self, app: GameContext) -> None:
        global PRESS_START_PROMPT

        super().__init__(app)

        self.prompt_font = createFont(48)

        self.animation_time: float = 0.0

        self.title_texture: pg.Surface = getTexture(tile_size=(1200, 368), source_path="./assets/sprites/spr_menu_title.png")

        self.prompt_texture: pg.Surface = self.prompt_font.render(
            PRESS_START_PROMPT,
            False,
            (255, 255, 255)
        )

        self.monsters: list[pg.Surface] = [
            getTexture((8, 0)),
            getTexture((0, 4)),
            getTexture((0, 7)),
            getTexture((9, 0))
        ]

        self.monsters_initial_time: list[float] = [
            random() * MENU_MONSTER_START_TIME_RANGE
            for _ in range(len(self.monsters))
        ]

        monster_index: int = 0
        self.monsters_width: int = MENU_MONSTER_SPRITE_GAP * (len(self.monsters) - 1)
        self.monsters_height: int = 0
        for monster in self.monsters:
            original_width, original_height = monster.get_size()

            new_width: int = int(original_width * MENU_MONSTER_SPRITE_SCALE)
            new_height: int = int(original_height * MENU_MONSTER_SPRITE_SCALE)

            self.monsters[monster_index] = pg.transform.scale(monster, (new_width, new_height))
            monster_index += 1

            self.monsters_width += new_width
            self.monsters_height = max(self.monsters_height, new_height)

    def enter(self) -> None:
        self.animation_time = 0.0

    def exit(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.animation_time += delta_time

    def draw(self, canvas: pg.Surface) -> None:
        canvas_width, canvas_height = canvas.get_size()

        title_width: int = self.title_texture.get_width()
        canvas.blit(self.title_texture, ((canvas_width - title_width) // 2, 0))

        prompt_width, prompt_height = self.prompt_texture.get_size()
        canvas.blit(self.prompt_texture, ((canvas_width - prompt_width) // 2, (canvas_height - prompt_height) // 2))

        monster_index: int = 0
        monster_x: int = (canvas_width - self.monsters_width) // 2
        monster_y: int = canvas_height - self.monsters_height - MENU_MONSTER_SPRITE_BUFFER_Y
        for monster in self.monsters:
            canvas.blit(
                monster,
                (
                    monster_x,
                    monster_y + MENU_MONSTER_BOB_DELTA * sin(self.animation_time + self.monsters_initial_time[monster_index])
                )
            )

            monster_x += monster.get_width() + MENU_MONSTER_SPRITE_GAP
            monster_index += 1

    def shouldTransition(self) -> bool:
        return (
            self.app.red_joystick.get_button(Input.START_BUTTON) or
            self.app.blue_joystick.get_button(Input.START_BUTTON)
        )