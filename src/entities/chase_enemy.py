import math
import pygame as pg
from .player import Player
from ..scenes import shared_config
from.maze_manager import MazeManager
from .__utils import performAStar, RAD_2_DEG

CHASE_PATH_POLL_TIME: float = 6.0
CHASE_PATH_ARRIVED_BUFFER: float = shared_config.GRID_CELL_SIZE * 0.05

CHASE_WALK_SPEED: float = shared_config.GRID_CELL_SIZE * 3.0

CHASE_COLLISION_RADIUS_SQR: float = shared_config.HALF_GRID_CELL_SIZE * shared_config.HALF_GRID_CELL_SIZE

class ChaseEnemy:
    def __init__(
        self,
        frame_time: float,
        animation_frames: list[pg.Surface],
        start_position: tuple[float, float]
    ) -> None:
        self.start_position: tuple[float, float] = start_position

        self.position_x: float = start_position[0]
        self.position_y: float = start_position[1]
        self.rotation: float = 0.0

        self.animation_index: int = 0
        self.animation_time: float = 0.0
        self.animation_direction: int = 1
        self.FRAME_TIME: float = frame_time
        self.animation_frames: list[pg.Surface] = animation_frames

        self.path_index: int = 0
        self.path_time: float = 0.0
        self.path: list[tuple[int, int]] = []

    def reset(self, target_position: tuple[float, float], maze: list[list[bool]]) -> None:
        self.position_x, self.position_y = self.start_position
        
        self.animation_index = 0
        self.animation_time = 0.0

        self.__selectNewPath(target_position, maze)

    def __checkPlayerCollision(self, player: Player, maze: MazeManager) -> None:
        if player.isDead():
            return
        
        x, y = player.getPosition()
        delta_x, delta_y = x - self.position_x, y - self.position_y
        dist_sqr: float = (delta_x * delta_x) + (delta_y * delta_y)

        if dist_sqr <= CHASE_COLLISION_RADIUS_SQR:
            maze.dropPurse((x, y), player.killPlayer())
            self.__selectNewPath(self.start_position, maze.getSolidMask())

    def __selectNewPath(self, target_position: tuple[float, float], maze: list[list[bool]]):
        self.path_index = 0
        self.path_time = 0.0

        int_initial_position: tuple[int, int] = (
            int((self.position_x + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE),
            int((self.position_y + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)
        )

        int_target_position: tuple[int, int] = (
            int((target_position[0] + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE),
            int((target_position[1] + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)
        )

        self.path = performAStar(int_initial_position, int_target_position, maze)

    def update(self, delta_time: float, target_player: Player, other_player: Player, maze: MazeManager) -> None:
        self.animation_time += delta_time
        if self.animation_time >= self.FRAME_TIME:
            self.animation_time -= self.FRAME_TIME
            self.animation_index += self.animation_direction

            if self.animation_index == 0 or self.animation_index == len(self.animation_frames) - 1:
                self.animation_direction *= -1

        if self.path_index < len(self.path):
            node_x_index, node_y_index = self.path[self.path_index]

            node_x: float = node_x_index * shared_config.GRID_CELL_SIZE
            node_y: float = node_y_index * shared_config.GRID_CELL_SIZE

            delta_x: float = node_x - self.position_x
            delta_y: float = node_y - self.position_y

            node_dist: float = math.sqrt((delta_x * delta_x) + (delta_y * delta_y))

            if node_dist <= CHASE_PATH_ARRIVED_BUFFER:
                self.path_index += 1
            else:
                self.position_x += delta_x * CHASE_WALK_SPEED * delta_time / node_dist
                self.position_y += delta_y * CHASE_WALK_SPEED * delta_time / node_dist

                self.rotation = 90.0 + math.atan2(delta_y, -delta_x) * RAD_2_DEG

            self.path_time += delta_time
            if self.path_time >= CHASE_PATH_POLL_TIME:
                self.__selectNewPath(target_player.getPosition(), maze.getSolidMask())
        else:
            self.__selectNewPath(target_player.getPosition(), maze.getSolidMask())

        self.__checkPlayerCollision(target_player, maze)
        self.__checkPlayerCollision(other_player, maze)

    def draw(self, canvas: pg.Surface) -> None:
        canvas.blit(
            pg.transform.rotate(
                self.animation_frames[self.animation_index],
                self.rotation
            ),
            (
                shared_config.GRID_RENDER_OFFSET_X + self.position_x,
                shared_config.GRID_RENDER_OFFSET_Y + self.position_y
            )
        )