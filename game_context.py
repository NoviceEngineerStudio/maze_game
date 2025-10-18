import pygame as pg
import dataclasses as dc

@dc.dataclass
class GameContext:
    canvas_width: int
    canvas_height: int
    canvas: pg.Surface