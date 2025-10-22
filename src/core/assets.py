import pygame as pg

__MASTER_TEXTURE_ATLAS_PATH: str = "./assets/spr_master_atlas.png"
__PIXELIFY_SANS_REGULAR_PATH: str = "./assets/fonts/PixelifySans-Regular.ttf"

__DEFAULT_TILE_SIZE_WIDTH: int = 32
__DEFAULT_TILE_SIZE_HEIGHT: int = 32
__DEFAULT_TILE_SIZE: tuple[int, int] = (__DEFAULT_TILE_SIZE_WIDTH, __DEFAULT_TILE_SIZE_HEIGHT)

def createFont(size: int, path: str | None = __PIXELIFY_SANS_REGULAR_PATH) -> pg.font.FontType:
    return pg.font.Font(path, size)

def getTexture(
        indices: tuple[int, int] = (0, 0),
        tile_size: tuple[int, int] = __DEFAULT_TILE_SIZE,
        source_path: str = __MASTER_TEXTURE_ATLAS_PATH
) -> pg.Surface:
    x_index, y_index = indices
    width, height = tile_size

    source_image: pg.Surface = pg.image.load(source_path).convert_alpha()

    return source_image.subsurface((
        x_index * width,
        y_index * height,
        width,
        height
    ))

def getTextures(
        row_count: int,
        column_count: int,
        in_row_order: bool = True,
        root_indices: tuple[int, int] = (0, 0),
        tile_size: tuple[int, int] = __DEFAULT_TILE_SIZE,
        source_path: str = __MASTER_TEXTURE_ATLAS_PATH
) -> list[pg.Surface]:
    x_index, y_index = root_indices
    width, height = tile_size

    source_image: pg.Surface = pg.image.load(source_path).convert_alpha()

    texture_index: int = 0
    textures: list[pg.Surface] = [pg.Surface((1, 1)) for _ in range(row_count * column_count)]

    if in_row_order:
        for column_index in range(column_count):
            for row_index in range(row_count):
                textures[texture_index] = source_image.subsurface((
                    (x_index + column_index) * width,
                    (y_index + row_index) * height,
                    width,
                    height
                ))

                texture_index += 1
    else:
        for row_index in range(row_count):
            for column_index in range(column_count):
                textures[texture_index] = source_image.subsurface((
                    (x_index + column_index) * width,
                    (y_index + row_index) * height,
                    width,
                    height
                ))

                texture_index += 1

    return textures