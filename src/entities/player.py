import math
import pygame as pg
from .maze_manager import PropType
from ..scenes import shared_config
from ..core import Input, getTextures

RAD_2_DEG: float = 180.0 / math.pi

PLAYER_WALK_SPEED: float = 4.0 * shared_config.GRID_CELL_SIZE
PLAYER_ANIMATION_FRAME_TIME: float = 0.1

PLAYER_COLLISION_RADIUS: float = shared_config.HALF_GRID_CELL_SIZE
PLAYER_COLLISION_RADIUS_SQR: float = PLAYER_COLLISION_RADIUS * PLAYER_COLLISION_RADIUS

RED_PLAYER_INITIAL_X: float = shared_config.GRID_CELL_SIZE * (shared_config.GRID_COLUMN_COUNT - 2)
RED_PLAYER_INITIAL_Y: float = shared_config.GRID_CELL_SIZE * (1 + (shared_config.GRID_ROW_COUNT - 2) // 2)
RED_PLAYER_INITIAL_ROTATION: float = 90.0

BLUE_PLAYER_INITIAL_X: float = shared_config.GRID_CELL_SIZE
BLUE_PLAYER_INITIAL_Y: float = RED_PLAYER_INITIAL_Y
BLUE_PLAYER_INITIAL_ROTATION: float = RED_PLAYER_INITIAL_ROTATION + 180.0

JOYSTICK_AXIS_THRESHOLD: float = 0.5

COIN_SCORE: int = 10
TREASURE_SCORE: int = COIN_SCORE * 10

STAR_POWER_DURATION: float = 10.0
DEATH_ANIMATION_TIME: float = 0.2

PURSE_DROP_AMMOUNT: int = 100

class Player:
    def __init__(self, is_red: bool, joystick: pg.joystick.JoystickType) -> None:
        self.is_red: bool = is_red
        self.joystick: pg.joystick.JoystickType = joystick

        self.score: int = 0
        self.is_dead: bool = False

        self.animation_index: int = 0
        self.animation_time: float = 0.0
        self.animation_frames: list[pg.Surface] = []
        self.star_power_frames: list[pg.Surface] = getTextures(1, 6, root_indices=(0, 9))
        self.death_frames: list[pg.Surface] = getTextures(1, 8, root_indices=(0, 8))

        self.star_power_active: bool = False
        self.star_power_time: float = 0.0

        self.position_x: float = 0.0
        self.position_y: float = 0.0

        self.rotation: float = 0.0

        self.input_x: float = 0.0
        self.input_y: float = 0.0
        self.input_factor_x: int = 1
        self.input_factor_y: int = 1

        if is_red:
            self.input_factor_y = -1

            self.animation_frames = getTextures(1, 6, root_indices=(0, 3))
        else:
            self.input_factor_x = -1

            self.animation_frames = getTextures(1, 6, root_indices=(0, 2))

    def reset(self) -> None:
        self.score = 0
        self.is_dead: bool = False

        self.star_power_active = False
        self.star_power_time = 0.0

        if self.is_red:
            self.position_x = RED_PLAYER_INITIAL_X
            self.position_y = RED_PLAYER_INITIAL_Y
            self.rotation = RED_PLAYER_INITIAL_ROTATION
        else:
            self.position_x = BLUE_PLAYER_INITIAL_X
            self.position_y = BLUE_PLAYER_INITIAL_Y
            self.rotation = BLUE_PLAYER_INITIAL_ROTATION

    def getScore(self) -> int:
        return self.score
    
    def getPosition(self) -> tuple[float, float]:
        return (self.position_x, self.position_y)
    
    def updateMovement(self, delta_time: float) -> None:
        if self.is_dead:
            self.animation_time += delta_time

            if self.animation_time < DEATH_ANIMATION_TIME:
                return
            
            self.animation_time -= DEATH_ANIMATION_TIME
            self.animation_index += 1

            if self.animation_index < len(self.death_frames):
                return
            
            self.is_dead = False
            self.animation_index = 0
            self.animation_time = 0.0

            if self.is_red:
                self.position_x = RED_PLAYER_INITIAL_X
                self.position_y = RED_PLAYER_INITIAL_Y
                self.rotation = RED_PLAYER_INITIAL_ROTATION
            else:
                self.position_x = BLUE_PLAYER_INITIAL_X
                self.position_y = BLUE_PLAYER_INITIAL_Y
                self.rotation = BLUE_PLAYER_INITIAL_ROTATION

        if self.star_power_active:
            self.star_power_time -= delta_time
            self.star_power_active = self.star_power_time > 0.0

        self.input_x: float = self.joystick.get_axis(Input.LEFT_STICK_Y_AXIS) * self.input_factor_x
        self.input_y: float = self.joystick.get_axis(Input.LEFT_STICK_X_AXIS) * self.input_factor_y

        if abs(self.input_x) > JOYSTICK_AXIS_THRESHOLD or abs(self.input_y) > JOYSTICK_AXIS_THRESHOLD:
            input_mag: float = math.sqrt((self.input_x * self.input_x) + (self.input_y * self.input_y))

            self.input_x /= input_mag
            self.input_y /= input_mag

            self.rotation = 90.0 + math.atan2(self.input_y, -self.input_x) * RAD_2_DEG

            self.position_x += self.input_x * PLAYER_WALK_SPEED * delta_time
            self.position_y += self.input_y * PLAYER_WALK_SPEED * delta_time

            self.animation_time += delta_time
            if self.animation_time >= PLAYER_ANIMATION_FRAME_TIME:
                self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
                self.animation_time -= PLAYER_ANIMATION_FRAME_TIME
        else:
            self.animation_index = 0
            self.animation_time = 0.0

    def handleWallCollisions(self, solid_mask: list[list[bool]]) -> None:
        map_x_index: int = int (self.position_x / shared_config.GRID_CELL_SIZE)
        map_y_index: int = int (self.position_y / shared_config.GRID_CELL_SIZE)

        for x in range(max(0, map_x_index - 1), min(shared_config.GRID_COLUMN_COUNT, map_x_index + 2)):
            for y in range(max(0, map_y_index - 1), min(shared_config.GRID_ROW_COUNT, map_y_index + 2)):
                if not solid_mask[x][y]:
                    continue

                tile_center_x: float = x * shared_config.GRID_CELL_SIZE + shared_config.HALF_GRID_CELL_SIZE
                tile_center_y: float = y * shared_config.GRID_CELL_SIZE + shared_config.HALF_GRID_CELL_SIZE

                player_center_x: float = self.position_x + PLAYER_COLLISION_RADIUS
                player_center_y: float = self.position_y + PLAYER_COLLISION_RADIUS

                delta_x: float = player_center_x - tile_center_x
                delta_y: float = player_center_y - tile_center_y

                inner_x: float = max(-shared_config.HALF_GRID_CELL_SIZE, min(delta_x, shared_config.HALF_GRID_CELL_SIZE))
                inner_y: float = max(-shared_config.HALF_GRID_CELL_SIZE, min(delta_y, shared_config.HALF_GRID_CELL_SIZE))

                closest_x: float = tile_center_x + inner_x
                closest_y: float = tile_center_y + inner_y

                distance_x: float = player_center_x - closest_x
                distance_y: float = player_center_y - closest_y
                sqr_distance: float = (distance_x * distance_x) + (distance_y * distance_y)

                if sqr_distance < PLAYER_COLLISION_RADIUS_SQR:
                    if sqr_distance > 0.0:
                        magnitude: float = math.sqrt(sqr_distance)
                        
                        normal_x: float = distance_x / magnitude
                        normal_y: float = distance_y / magnitude

                        penetration: float = PLAYER_COLLISION_RADIUS - magnitude

                        self.position_x += normal_x * penetration
                        self.position_y += normal_y * penetration
                    else:
                        self.position_x = closest_x + self.input_x * PLAYER_COLLISION_RADIUS
                        self.position_y = closest_y + self.input_y * PLAYER_COLLISION_RADIUS

    def applyProp(self, prop: PropType, prop_payload: int) -> None:
        match prop:
            case PropType.COIN:
                self.score += COIN_SCORE
            case PropType.TREASURE:
                self.score += TREASURE_SCORE
            case PropType.PURSE:
                self.score += prop_payload
            case PropType.STAR:
                self.star_power_active = True
                self.star_power_time = STAR_POWER_DURATION
            case _:
                pass

    def killPlayer(self) -> int:
        # ? Cannot Die with Invincibility or if Already
        if self.star_power_active or self.is_dead:
            return 0
        
        self.is_dead = True
        self.animation_index = 0
        self.animation_time = 0.0

        drop_ammount: int = min(self.score, PURSE_DROP_AMMOUNT)
        self.score -= drop_ammount

        return drop_ammount

    def draw(self, canvas: pg.Surface) -> None:
        if self.is_dead:
            canvas.blit(
                self.death_frames[self.animation_index],
                (
                    shared_config.GRID_RENDER_OFFSET_X + self.position_x,
                    shared_config.GRID_RENDER_OFFSET_Y + self.position_y
                )
            )

            return

        base_texture: pg.Surface = (
            self.star_power_frames[self.animation_index] if self.star_power_active
            else self.animation_frames[self.animation_index]
        )

        canvas.blit(
            pg.transform.rotate(base_texture, self.rotation),
            (
                shared_config.GRID_RENDER_OFFSET_X + self.position_x,
                shared_config.GRID_RENDER_OFFSET_Y + self.position_y
            )
        )