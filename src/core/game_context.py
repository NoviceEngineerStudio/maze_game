import pygame as pg
from dataclasses import dataclass

@dataclass
class GameContext:
    window_surface: pg.Surface
    render_surface: pg.Surface

    red_joystick: pg.joystick.JoystickType
    blue_joystick: pg.joystick.JoystickType