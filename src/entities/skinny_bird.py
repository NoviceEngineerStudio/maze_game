import math
import pygame as pg
from random import random
from .player import Player
from ..core import getTextures
from ..scenes import shared_config
from .maze_manager import MazeManager

SKINNY_BIRD_MOVE_TIME: float = 10.0
SKINNY_BIRD_ANIMATION_TIME: float = 0.15

SKINNY_BIRD_INITIAL_X: float = 21.0 * shared_config.GRID_CELL_SIZE
SKINNY_BIRD_INITIAL_Y: float = 11.0 * shared_config.GRID_CELL_SIZE

SKINNY_BIRD_MOVE_BUFFER: float = shared_config.GRID_CELL_SIZE * 6.0

SKINNY_BIRD_COLLISION_RADIUS_SQR = shared_config.HALF_GRID_CELL_SIZE * shared_config.HALF_GRID_CELL_SIZE

class SkinnyBird:
    def __init__(self) -> None:
        self.move_time: float = 0.0

        self.position_x: float = 0.0
        self.position_y: float = 0.0

        self.animation_time: float = 0.0
        self.animation_index: int = 0
        self.animation_direction: int = 1
        self.animation_frames: list[pg.Surface] = getTextures(1, 4, root_indices=(0, 5))

    def reset(self) -> None:
        self.move_time = 0.0

        self.position_x = SKINNY_BIRD_INITIAL_X
        self.position_y = SKINNY_BIRD_INITIAL_Y

        self.animation_time = 0.0
        self.animation_index = 0
        self.animation_direction = 1

    def __checkPlayerCollision(self, player: Player, maze: MazeManager) -> None:
        if player.isDead():
            return
        
        x, y = player.getPosition()
        delta_x, delta_y = x - self.position_x, y - self.position_y
        dist_sqr: float = (delta_x * delta_x) + (delta_y * delta_y)

        if dist_sqr <= SKINNY_BIRD_COLLISION_RADIUS_SQR:
            maze.dropPurse((x, y), player.killPlayer())

    def __selectNewPosition(self, red_player: Player, blue_player: Player, maze: MazeManager) -> None:
        red_x, red_y = red_player.getPosition()
        blue_x, blue_y = blue_player.getPosition()

        origin_x: float = red_x
        origin_y: float = red_y

        if random() < 0.5:
            origin_x = blue_x
            origin_y = blue_y

        rand_angle: float = random() * 2.0 * math.pi
        target_x: float = origin_x + math.sin(rand_angle) * SKINNY_BIRD_MOVE_BUFFER
        target_y: float = origin_y + math.cos(rand_angle) * SKINNY_BIRD_MOVE_BUFFER

        solid_mask: list[list[bool]] = maze.getSolidMask()

        x_index: int = max(0, min(
            int(target_x / shared_config.GRID_CELL_SIZE),
            shared_config.GRID_COLUMN_COUNT - 1
        ))
        y_index: int = max(0, min(
            int(target_y / shared_config.GRID_CELL_SIZE),
            shared_config.GRID_ROW_COUNT - 1
        ))

        for _ in range(shared_config.GRID_ROW_COUNT):
            if not solid_mask[x_index][y_index]:
                self.position_x = x_index * shared_config.GRID_CELL_SIZE
                self.position_y = y_index * shared_config.GRID_CELL_SIZE
                return
            
            y_index = (y_index + 1) % shared_config.GRID_ROW_COUNT

    def update(self, delta_time: float, red_player: Player, blue_player: Player, maze: MazeManager) -> None:
        self.move_time += delta_time
        self.animation_time += delta_time

        if self.move_time >= SKINNY_BIRD_MOVE_TIME:
            self.move_time -= SKINNY_BIRD_MOVE_TIME
            self.__selectNewPosition(red_player, blue_player, maze)

        if self.animation_time >= SKINNY_BIRD_ANIMATION_TIME:
            self.animation_time -= SKINNY_BIRD_ANIMATION_TIME
            self.animation_index += self.animation_direction

            if self.animation_index == 0 or self.animation_index == len(self.animation_frames) - 1:
                self.animation_direction *= -1

        self.__checkPlayerCollision(red_player, maze)
        self.__checkPlayerCollision(blue_player, maze)
            
    def draw(self, canvas: pg.Surface) -> None:
        canvas.blit(
            self.animation_frames[self.animation_index],
            (
                shared_config.GRID_RENDER_OFFSET_X + self.position_x,
                shared_config.GRID_RENDER_OFFSET_Y + self.position_y
            )
        )