import math
import pygame as pg
from random import random
from .player import Player
from typing import Callable
from ..core import getTextures
from ..scenes import shared_config
from .maze_manager import MazeManager
from .__utils import RAD_2_DEG, performAStar

NOBODY_INITIAL_X: float = 23.0 * shared_config.GRID_CELL_SIZE
NOBODY_INITIAL_Y: float = 13.0 * shared_config.GRID_CELL_SIZE

NOBODY_PATROL_FRAME_TIME: float = 0.15
NOBODY_CROUCH_FRAME_TIME: float = 0.2
NOBODY_ROLL_FRAME_TIME: float = 0.1

NOBODY_WALK_SPEED: float = shared_config.GRID_CELL_SIZE * 2.0
NOBODY_ROLL_SPEED: float = shared_config.GRID_CELL_SIZE * 3.75

NOBODY_COLLISION_RADIUS_SQR: float = shared_config.HALF_GRID_CELL_SIZE * shared_config.HALF_GRID_CELL_SIZE

NOBODY_PATH_ARRIVED_BUFFER: float = shared_config.GRID_CELL_SIZE * 0.05

class NobodyRollyPolly:
    def __init__(self) -> None:
        self.position_x: float = 0.0
        self.position_y: float = 0.0
        self.rotation: float = 0.0

        self.patrol_frames: list[pg.Surface] = getTextures(3, 1, False, (9, 0))
        self.crouch_frames: list[pg.Surface] = getTextures(3, 1, False, (9, 3))
        self.roll_frames: list[pg.Surface] = getTextures(6, 1, False, (9, 5))

        self.animation_index: int = 0
        self.animation_time: float = 0.0
        self.animation_direction: int = 1
        self.active_frames: list[pg.Surface] = self.patrol_frames

        self.path_index: int = 0
        self.path: list[tuple[int, int]] = []

        self.hit_player: bool = False
        self.roll_position: tuple[int, int] = (0, 0)

        self.roll_x_delta: int = 0
        self.roll_y_delta: int = 0

        self.updateState: Callable[[float, Player, Player, MazeManager], None] = self.updatePatrolState

    def reset(self, maze: list[list[bool]]) -> None:
        self.position_x = NOBODY_INITIAL_X
        self.position_y = NOBODY_INITIAL_Y

        self.enterPatrolState(maze)

    def __checkPlayerCollision(self, player: Player, maze: MazeManager) -> None:
        if player.isDead():
            return
        
        x, y = player.getPosition()
        delta_x, delta_y = x - self.position_x, y - self.position_y
        dist_sqr: float = (delta_x * delta_x) + (delta_y * delta_y)

        if dist_sqr <= NOBODY_COLLISION_RADIUS_SQR:
            maze.dropPurse((x, y), player.killPlayer())
            self.hit_player = True

    def update(
        self,
        delta_time: float,
        red_player: Player,
        blue_player: Player,
        maze: MazeManager
    ) -> None:
        self.animation_time += delta_time
        self.__checkPlayerCollision(red_player, maze)
        self.__checkPlayerCollision(blue_player, maze)
        self.updateState(delta_time, red_player, blue_player, maze)

    def draw(self, canvas: pg.Surface) -> None:
        canvas.blit(
            pg.transform.rotate(
                self.active_frames[self.animation_index],
                self.rotation
            ),
            (
                shared_config.GRID_RENDER_OFFSET_X + self.position_x,
                shared_config.GRID_RENDER_OFFSET_Y + self.position_y
            )
        )

    def __animateBackAndForth(self, frame_time: float) -> bool:
        if self.animation_time >= frame_time:
            self.animation_time -= frame_time
            self.animation_index += self.animation_direction

            if self.animation_index == 0 or self.animation_index == len(self.active_frames) - 1:
                self.animation_direction *= -1
                return True
            
        return False

    def __animateLooping(self, frame_time: float) -> bool:
        if self.animation_time >= frame_time:
            self.animation_time -= frame_time
            self.animation_index += self.animation_direction

            if self.animation_index >= len(self.active_frames):
                self.animation_index = 0
                return True
            
            if self.animation_index < 0:
                self.animation_index = len(self.active_frames) - 1
                return True
            
        return False
    
    def __followPath(self, delta_time: float, move_speed: float) -> bool:
        if self.path_index < len(self.path):
            node_x_index, node_y_index = self.path[self.path_index]

            node_x: float = node_x_index * shared_config.GRID_CELL_SIZE
            node_y: float = node_y_index * shared_config.GRID_CELL_SIZE

            delta_x: float = node_x - self.position_x
            delta_y: float = node_y - self.position_y

            node_dist: float = math.sqrt((delta_x * delta_x) + (delta_y * delta_y))

            if node_dist <= NOBODY_PATH_ARRIVED_BUFFER:
                self.path_index += 1
            else:
                self.position_x += delta_x * move_speed * delta_time / node_dist
                self.position_y += delta_y * move_speed * delta_time / node_dist

                self.rotation = 270.0 + math.atan2(delta_y, -delta_x) * RAD_2_DEG

            return False
        
        return True

    ########################################
    # Patrol State                         #
    ########################################

    def __selectPatrolPath(self, maze: list[list[bool]]) -> None:
        int_initial_position: tuple[int, int] = (
            int((self.position_x + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE),
            int((self.position_y + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)
        )

        target_x: int = int(random() * shared_config.GRID_COLUMN_COUNT)
        target_y: int = int(random() * shared_config.GRID_ROW_COUNT)

        for _ in range(shared_config.GRID_COLUMN_COUNT):
            found_floor: bool = False

            for _ in range(shared_config.GRID_ROW_COUNT):
                if not maze[target_x][target_y]:
                    found_floor = True
                    break

                target_y = (target_y + 1) % shared_config.GRID_ROW_COUNT

            if found_floor:
                break

            target_x = (target_x + 1) % shared_config.GRID_COLUMN_COUNT

        self.path_index = 0
        self.path = performAStar(int_initial_position, (target_x, target_y), maze)

    def __hasLineOfSight(self, player_position: tuple[float, float], maze: list[list[bool]]) -> bool:
        player_x, player_y = player_position

        int_x: int = int((self.position_x + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)
        int_y: int = int((self.position_y + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)

        int_player_x: int = int((player_x + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)
        int_player_y: int = int((player_y + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)

        if int_x == int_player_x:
            min_y: int = 0
            max_y: int = 0

            if int_y < int_player_y:
                min_y = int_y
                max_y = int_player_y
                self.roll_y_delta = 1
            else:
                min_y = int_player_y
                max_y = int_y
                self.roll_y_delta = -1

            found_wall: bool = False
            for y in range(min_y, max_y + 1):
                if maze[int_x][y]:
                    found_wall = True
                    break

            if not found_wall:
                self.roll_position = (int_player_x, int_player_y)
                self.roll_x_delta = 0
                return True
            
        if int_y == int_player_y:
            min_x: int = 0
            max_x: int = 0

            if int_x < int_player_x:
                min_x = int_x
                max_x = int_player_x
                self.roll_x_delta = 1
            else:
                min_x = int_player_x
                max_x = int_x
                self.roll_x_delta = -1

            found_wall: bool = False
            for x in range(min_x, max_x + 1):
                if maze[x][int_y]:
                    found_wall = True
                    break

            if not found_wall:
                self.roll_position = (int_player_x, int_player_y)
                self.roll_y_delta = 0
                return True

        return False

    def enterPatrolState(self, maze: list[list[bool]]) -> None:
        self.updateState = self.updatePatrolState

        self.animation_index = 0
        self.animation_time = 0.0
        self.animation_direction = 1
        self.active_frames = self.patrol_frames

        self.__selectPatrolPath(maze)

    def updatePatrolState(
        self,
        delta_time: float,
        red_player: Player,
        blue_player: Player,
        maze: MazeManager
    ) -> None:
        self.__animateBackAndForth(NOBODY_PATROL_FRAME_TIME)

        if not red_player.isDead():
            if self.__hasLineOfSight(red_player.getPosition(), maze.getSolidMask()):
                self.enterCrouchState()
                return
        
        if not blue_player.isDead():
            if self.__hasLineOfSight(blue_player.getPosition(), maze.getSolidMask()):
                self.enterCrouchState()
                return

        if self.__followPath(delta_time, NOBODY_WALK_SPEED):
            self.__selectPatrolPath(maze.getSolidMask())

    ########################################
    # Crouch State                         #
    ########################################

    def enterCrouchState(self) -> None:
        self.updateState = self.updateCrouchState

        self.animation_index = 0
        self.animation_time = 0.0
        self.animation_direction = 1
        self.active_frames = self.crouch_frames

    def updateCrouchState(
        self,
        delta_time: float,
        red_player: Player,
        blue_player: Player,
        maze: MazeManager
    ) -> None:
        if self.__animateLooping(NOBODY_CROUCH_FRAME_TIME):
            self.enterRollState(maze.getSolidMask())

    ########################################
    # Roll State                           #
    ########################################

    def enterRollState(self, maze: list[list[bool]]) -> None:
        self.updateState = self.updateRollState

        self.animation_index = 0
        self.animation_time = 0.0
        self.animation_direction = 1
        self.active_frames = self.roll_frames

        self.hit_player = False

        if abs(self.roll_x_delta) > 0 or abs(self.roll_y_delta) > 0:
            roll_x, roll_y = self.roll_position

            while 0 < roll_x < shared_config.GRID_COLUMN_COUNT - 1 and 0 < roll_y < shared_config.GRID_ROW_COUNT - 1:
                if maze[roll_x + self.roll_x_delta][roll_y + self.roll_y_delta]:
                    break

                roll_x += self.roll_x_delta
                roll_y += self.roll_y_delta

            self.roll_position = (roll_x, roll_y)

        self.path_index = 0
        self.path = [self.roll_position]

    def updateRollState(
        self,
        delta_time: float,
        red_player: Player,
        blue_player: Player,
        maze: MazeManager
    ) -> None:
        self.__animateLooping(NOBODY_ROLL_FRAME_TIME)

        if self.hit_player:
            self.enterHitState()
            return

        if self.__followPath(delta_time, NOBODY_ROLL_SPEED):
            self.enterHitState()
            return

    ########################################
    # Hit State                            #
    ########################################

    def enterHitState(self) -> None:
        self.updateState = self.updateHitState

        self.animation_index = len(self.crouch_frames) - 1
        self.animation_time = 0.0
        self.animation_direction = -1
        self.active_frames = self.crouch_frames

    def updateHitState(
        self,
        delta_time: float,
        red_player: Player,
        blue_player: Player,
        maze: MazeManager
    ) -> None:
        if self.__animateLooping(NOBODY_CROUCH_FRAME_TIME):
            self.enterPatrolState(maze.getSolidMask())