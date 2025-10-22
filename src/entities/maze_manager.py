import os
import pygame as pg
from random import random
from ..core import getTextures
from ..scenes import shared_config

MAZE_LAYOUT_FILE_EXTENSION: str = ".png"
MAZE_LAYOUT_FOLDER_PATH: str = "./assets/mazes/"

FLOOR_VARIANT_PROBABILITY: float = 0.05
WALL_VARIANT_PROBABILITY: float = 0.05

class MazeManager:
    def __init__(self) -> None:
        self.solid_mask: list[list[bool]] = [
            [False for _ in range(shared_config.GRID_ROW_COUNT)]
            for _ in range(shared_config.GRID_COLUMN_COUNT)
        ]

        self.tiles_image: pg.Surface = pg.Surface((
            shared_config.GRID_COLUMN_COUNT * shared_config.GRID_CELL_SIZE,
            shared_config.GRID_ROW_COUNT * shared_config.GRID_CELL_SIZE
        ))

        self.wall_textures: list[pg.Surface] = getTextures(1, 8, root_indices=(0, 0))
        self.floor_textures: list[pg.Surface] = getTextures(1, 9, root_indices=(0, 1))

        self.layout_file_paths: list[str] = []
        for sub_path in os.listdir(MAZE_LAYOUT_FOLDER_PATH):
            full_sub_path: str = os.path.join(MAZE_LAYOUT_FOLDER_PATH, sub_path)

            if sub_path.endswith(MAZE_LAYOUT_FILE_EXTENSION) and not os.path.isdir(full_sub_path):
                self.layout_file_paths.append(full_sub_path)

        assert len(self.layout_file_paths) > 0

    def reset(self) -> None:
        layout_index: int = int(random() * len(self.layout_file_paths))
        layout: pg.Surface = pg.image.load(self.layout_file_paths[layout_index])

        layout_width, layout_height = layout.get_size()
        assert layout_width >= shared_config.GRID_COLUMN_COUNT
        assert layout_height >= shared_config.GRID_ROW_COUNT

        for x in range(shared_config.GRID_COLUMN_COUNT):
            for y in range(shared_config.GRID_ROW_COUNT):
                color: pg.Color = layout.get_at((x, y))

                if color.r < 128:
                    self.solid_mask[x][y] = True

                    texture_index: int = 0
                    if random() <= WALL_VARIANT_PROBABILITY:
                        texture_index = int(random() * len(self.wall_textures))

                    self.tiles_image.blit(
                        self.wall_textures[texture_index],
                        (x * shared_config.GRID_CELL_SIZE, y * shared_config.GRID_CELL_SIZE)
                    )
                else:
                    self.solid_mask[x][y] = False

                    texture_index: int = 0
                    if random() <= FLOOR_VARIANT_PROBABILITY:
                        texture_index = int(random() * len(self.wall_textures))

                    self.tiles_image.blit(
                        self.floor_textures[texture_index],
                        (x * shared_config.GRID_CELL_SIZE, y * shared_config.GRID_CELL_SIZE)
                    )

    def update(self, delta_time: float) -> None:
        pass

    def getSolidMask(self) -> list[list[bool]]:
        return self.solid_mask

    def drawMaze(self, canvas: pg.Surface) -> None:
        canvas.blit(self.tiles_image, (shared_config.GRID_RENDER_OFFSET_X, shared_config.GRID_RENDER_OFFSET_Y))

    def drawProps(self, canvas: pg.Surface) -> None:
        pass

    def drawShimmers(self, canvas: pg.Surface) -> None:
        pass