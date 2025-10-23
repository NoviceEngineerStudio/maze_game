import os
import pygame as pg
from enum import IntEnum
from random import random
from ..scenes import shared_config
from ..core import getTextures, getTexture

MAZE_LAYOUT_FILE_EXTENSION: str = ".png"
MAZE_LAYOUT_FOLDER_PATH: str = "./assets/mazes/"

FLOOR_VARIANT_PROBABILITY: float = 0.05
WALL_VARIANT_PROBABILITY: float = 0.05

COIN_ANIMATION_TIME: float = 0.15
STAR_ANIMATION_TIME: float = 0.15
SHIMMER_ANIMATION_TIME: float = 0.1

class PropType(IntEnum):
    NONE = 0
    COIN = 1
    TREASURE = 2
    PURSE = 3
    STAR = 4

class MazeManager:
    def __init__(self) -> None:
        self.solid_mask: list[list[bool]] = [
            [False for _ in range(shared_config.GRID_ROW_COUNT)]
            for _ in range(shared_config.GRID_COLUMN_COUNT)
        ]

        self.prop_mask: list[list[PropType]] = [
            [PropType.NONE for _ in range(shared_config.GRID_ROW_COUNT)]
            for _ in range(shared_config.GRID_COLUMN_COUNT)
        ]

        self.tiles_image: pg.Surface = pg.Surface((
            shared_config.GRID_COLUMN_COUNT * shared_config.GRID_CELL_SIZE,
            shared_config.GRID_ROW_COUNT * shared_config.GRID_CELL_SIZE
        ))

        self.wall_textures: list[pg.Surface] = getTextures(1, 8, root_indices=(0, 0))
        self.floor_textures: list[pg.Surface] = getTextures(1, 9, root_indices=(0, 1))

        self.coin_textures: list[pg.Surface] = getTextures(1, 4, root_indices=(0, 6))
        self.star_textures: list[pg.Surface] = getTextures(4, 2, False, (6, 3))

        self.chest_texture: pg.Surface = getTexture((6, 2))
        self.purse_texture: pg.Surface = getTexture((7, 2))

        self.shimmer_textures: list[pg.Surface] = getTextures(6, 1, False, (8, 2))

        self.coin_positions: list[tuple[int, int]] = []
        self.treasure_positions: list[tuple[int, int]] = []
        self.purse_positions: list[tuple[int, int]] = []
        self.star_positions: list[tuple[int, int]] = []

        self.purse_payloads: dict[tuple[int, int], int] = dict[tuple[int, int], int]()

        self.coin_animation_time: float = 0.0
        self.star_animation_time: float = 0.0
        self.shimmer_animation_time: float = 0.0

        self.coin_animation_index: int = 0
        self.star_animation_index: int = 0
        self.shimmer_animation_index: int = 0

        self.coin_animation_direction: int = 1

        self.layout_file_paths: list[str] = []
        for sub_path in os.listdir(MAZE_LAYOUT_FOLDER_PATH):
            full_sub_path: str = os.path.join(MAZE_LAYOUT_FOLDER_PATH, sub_path)

            if sub_path.endswith(MAZE_LAYOUT_FILE_EXTENSION) and not os.path.isdir(full_sub_path):
                self.layout_file_paths.append(full_sub_path)

        assert len(self.layout_file_paths) > 0

    def reset(self) -> None:
        self.coin_animation_time = 0.0
        self.star_animation_time = 0.0
        self.shimmer_animation_time = 0.0

        self.coin_animation_index = 0
        self.star_animation_index = 0
        self.shimmer_animation_index = 0

        self.coin_animation_direction = 1

        self.coin_positions.clear()
        self.treasure_positions.clear()
        self.purse_positions.clear()
        self.star_positions.clear()
        self.purse_payloads.clear()

        layout_index: int = int(random() * len(self.layout_file_paths))
        layout: pg.Surface = pg.image.load(self.layout_file_paths[layout_index])

        layout_width, layout_height = layout.get_size()
        assert layout_width >= shared_config.GRID_COLUMN_COUNT
        assert layout_height >= shared_config.GRID_ROW_COUNT

        for x in range(shared_config.GRID_COLUMN_COUNT):
            for y in range(shared_config.GRID_ROW_COUNT):
                color: pg.Color = layout.get_at((x, y))
                color_code: int = (color.r << 16) | (color.g << 8) | (color.b)

                self.prop_mask[x][y] = PropType.NONE

                if color.r == 255:
                    self.solid_mask[x][y] = False

                    texture_index: int = 0
                    if random() <= FLOOR_VARIANT_PROBABILITY:
                        texture_index = int(random() * len(self.wall_textures))

                    self.tiles_image.blit(
                        self.floor_textures[texture_index],
                        (x * shared_config.GRID_CELL_SIZE, y * shared_config.GRID_CELL_SIZE)
                    )

                match color_code:
                    case 0x000000:
                        self.solid_mask[x][y] = True

                        texture_index: int = 0
                        if random() <= WALL_VARIANT_PROBABILITY:
                            texture_index = int(random() * len(self.wall_textures))

                        self.tiles_image.blit(
                            self.wall_textures[texture_index],
                            (x * shared_config.GRID_CELL_SIZE, y * shared_config.GRID_CELL_SIZE)
                        )
                    case 0xFF0000:
                        self.star_positions.append((x, y))
                        self.prop_mask[x][y] = PropType.STAR
                    case 0xFF00FF:
                        self.treasure_positions.append((x, y))
                        self.prop_mask[x][y] = PropType.TREASURE
                    case 0xFFFF00:
                        self.coin_positions.append((x, y))
                        self.prop_mask[x][y] = PropType.COIN
                    case _:
                        pass

    def update(self, delta_time: float) -> None:
        self.coin_animation_time += delta_time
        self.star_animation_time += delta_time
        self.shimmer_animation_time += delta_time

        if self.coin_animation_time >= COIN_ANIMATION_TIME:
            self.coin_animation_time -= COIN_ANIMATION_TIME

            self.coin_animation_index += self.coin_animation_direction

            if self.coin_animation_index == 0 or self.coin_animation_index == len(self.coin_textures) - 1:
                self.coin_animation_direction *= -1

        if self.star_animation_time >= STAR_ANIMATION_TIME:
            self.star_animation_time -= STAR_ANIMATION_TIME
            self.star_animation_index = (self.star_animation_index + 1) % len(self.star_textures)

        if self.shimmer_animation_time >= SHIMMER_ANIMATION_TIME:
            self.shimmer_animation_time -= SHIMMER_ANIMATION_TIME
            self.shimmer_animation_index = (self.shimmer_animation_index + 1) % len(self.shimmer_textures)

    def handleCollection(self, position: tuple[float, float]) -> tuple[PropType, int]:
        position_x, position_y = position
        center_x, center_y = position_x + shared_config.HALF_GRID_CELL_SIZE, position_y + shared_config.HALF_GRID_CELL_SIZE

        x, y = int(center_x / shared_config.GRID_CELL_SIZE), int(center_y / shared_config.GRID_CELL_SIZE)

        if 0 <= x < shared_config.GRID_COLUMN_COUNT and 0 <= y < shared_config.GRID_ROW_COUNT:
            payload: int = 0
            prop: PropType = self.prop_mask[x][y]
            self.prop_mask[x][y] = PropType.NONE
            
            match prop:
                case PropType.COIN:
                    self.coin_positions.remove((x, y))
                case PropType.TREASURE:
                    self.treasure_positions.remove((x, y))
                case PropType.PURSE:
                    self.purse_positions.remove((x, y))
                    purse_ammount: int | None = self.purse_payloads.get((x, y))
                    if not purse_ammount is None:
                        payload = purse_ammount
                case PropType.STAR:
                    self.star_positions.remove((x, y))
                case _:
                    pass

            return (prop, payload)
        
        return (PropType.NONE, 0)

    def dropPurse(self, position: tuple[float, float], purse_ammount: int) -> None:
        if purse_ammount <= 0:
            return
        
        position_x, position_y = position
        x: int = int((position_x + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)
        y: int = int((position_y + shared_config.HALF_GRID_CELL_SIZE) / shared_config.GRID_CELL_SIZE)

        if 0 <= x < shared_config.GRID_COLUMN_COUNT and 0 <= y < shared_config.GRID_ROW_COUNT:
            self.prop_mask[x][y] = PropType.PURSE
            self.purse_positions.append((x, y))
            self.purse_payloads[(x, y)] = purse_ammount

    def getSolidMask(self) -> list[list[bool]]:
        return self.solid_mask

    def drawMaze(self, canvas: pg.Surface) -> None:
        canvas.blit(self.tiles_image, (shared_config.GRID_RENDER_OFFSET_X, shared_config.GRID_RENDER_OFFSET_Y))

    def drawProps(self, canvas: pg.Surface) -> None:
        coin_frame: pg.Surface = self.coin_textures[self.coin_animation_index]
        for x, y in self.coin_positions:
            canvas.blit(
                coin_frame,
                (
                    x * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_X,
                    y * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_Y
                )
            )

        for x, y in self.treasure_positions:
            canvas.blit(
                self.chest_texture,
                (
                    x * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_X,
                    y * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_Y
                )
            )

        for x, y in self.purse_positions:
            canvas.blit(
                self.purse_texture,
                (
                    x * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_X,
                    y * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_Y
                )
            )

        star_frame: pg.Surface = self.star_textures[self.star_animation_index]
        for x, y in self.star_positions:
            canvas.blit(
                star_frame,
                (
                    x * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_X,
                    y * shared_config.GRID_CELL_SIZE + shared_config.GRID_RENDER_OFFSET_Y
                )
            )

    def drawShimmers(self, canvas: pg.Surface) -> None:
        shimmer_frame: pg.Surface = self.shimmer_textures[self.shimmer_animation_index]

        for x, y in self.treasure_positions:
            canvas.blit(
                shimmer_frame,
                (
                    x * shared_config.GRID_CELL_SIZE,
                    y * shared_config.GRID_CELL_SIZE
                )
            )

        for x, y in self.purse_positions:
            canvas.blit(
                shimmer_frame,
                (
                    x * shared_config.GRID_CELL_SIZE,
                    y * shared_config.GRID_CELL_SIZE
                )
            )

        for x, y in self.star_positions:
            canvas.blit(
                shimmer_frame,
                (
                    x * shared_config.GRID_CELL_SIZE,
                    y * shared_config.GRID_CELL_SIZE
                )
            )