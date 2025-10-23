import pygame as pg
from .scene import Scene
from ..scenes import shared_config
from .conclusion_scene import ConclusionScene
from ..core import GameContext, createFont, getTextures, getTexture
from ..entities import Player, MazeManager, SkinnyBird, NobodyRollyPolly, ChaseEnemy

GAME_DURATION: float = 45.0

GAME_UI_BUFFER_X: int = 8
GAME_UI_BUFFER_Y: int = 16

MASON_MANTIS_FRAME_TIME: float = 0.25
SCORP_DRAGON_FRAME_TIME: float = 0.15

MASON_MANTIS_INITIAL_X: float = 23.0 * shared_config.GRID_CELL_SIZE
MASON_MANTIS_INITIAL_Y: float = 11.0 * shared_config.GRID_CELL_SIZE

SCORP_DRAGON_INITIAL_X: float = 21.0 * shared_config.GRID_CELL_SIZE
SCORP_DRAGON_INITIAL_Y: float = 13.0 * shared_config.GRID_CELL_SIZE

class GameScene(Scene):
    def __init__(self, app: GameContext, conclusion_scene: ConclusionScene) -> None:
        super().__init__(app)

        self.conclusion_scene = conclusion_scene

        self.flashlight_mask: pg.Surface = pg.Surface((
            shared_config.GRID_CELL_SIZE * shared_config.GRID_COLUMN_COUNT,
            shared_config.GRID_CELL_SIZE * shared_config.GRID_ROW_COUNT
        ))

        self.flashlight_texture: pg.Surface = getTexture(tile_size=(480, 480), source_path="./assets/sprites/spr_flashlight_fade.png")

        self.game_time: float = 0.0

        self.red_player: Player = Player(True, app.red_joystick)
        self.blue_player: Player = Player(False, app.blue_joystick)

        self.maze_manager: MazeManager = MazeManager()

        self.skinny_bird: SkinnyBird = SkinnyBird()

        self.rolly_polly: NobodyRollyPolly = NobodyRollyPolly()

        self.mason_mantis: ChaseEnemy = ChaseEnemy(
            MASON_MANTIS_FRAME_TIME,
            getTextures(1, 6, root_indices=(2, 7)),
            (MASON_MANTIS_INITIAL_X, MASON_MANTIS_INITIAL_Y)
        )
        self.scorp_dragon: ChaseEnemy = ChaseEnemy(
            SCORP_DRAGON_FRAME_TIME,
            getTextures(1, 4, root_indices=(1, 4)),
            (SCORP_DRAGON_INITIAL_X, SCORP_DRAGON_INITIAL_Y)
        )

        self.ui_font: pg.font.FontType = createFont(56)

    def enter(self) -> None:
        self.game_time = GAME_DURATION

        self.red_player.reset()
        self.blue_player.reset()

        self.maze_manager.reset()

        self.skinny_bird.reset()

        self.rolly_polly.reset(self.maze_manager.getSolidMask())

        self.mason_mantis.reset(self.red_player.getPosition(), self.maze_manager.getSolidMask())
        self.scorp_dragon.reset(self.blue_player.getPosition(), self.maze_manager.getSolidMask())

    def exit(self) -> None:
        self.conclusion_scene.setFinalScores(
            self.red_player.getScore(),
            self.blue_player.getScore()
        )

    def update(self, delta_time: float) -> None:
        self.game_time -= delta_time
        if self.game_time < 0.0:
            self.game_time = 0.0

        self.maze_manager.update(delta_time)

        self.red_player.update(delta_time)
        self.blue_player.update(delta_time)

        if not self.red_player.isDead():
            self.red_player.handleWallCollisions(self.maze_manager.getSolidMask())
            red_prop, red_prop_payload = self.maze_manager.handleCollection(self.red_player.getPosition())
            self.red_player.applyProp(red_prop, red_prop_payload)

        if not self.blue_player.isDead():
            self.blue_player.handleWallCollisions(self.maze_manager.getSolidMask())
            blue_prop, blue_prop_payload = self.maze_manager.handleCollection(self.blue_player.getPosition())
            self.blue_player.applyProp(blue_prop, blue_prop_payload)

        self.skinny_bird.update(delta_time, self.red_player, self.blue_player, self.maze_manager)

        self.rolly_polly.update(delta_time, self.red_player, self.blue_player, self.maze_manager)

        self.mason_mantis.update(delta_time, self.red_player, self.blue_player, self.maze_manager)
        self.scorp_dragon.update(delta_time, self.blue_player, self.red_player, self.maze_manager)

    def draw(self, canvas: pg.Surface) -> None:
        canvas_width, canvas_height = canvas.get_size()

        self.maze_manager.drawMaze(canvas)
        self.maze_manager.drawProps(canvas)

        self.skinny_bird.draw(canvas)

        self.rolly_polly.draw(canvas)

        self.mason_mantis.draw(canvas)
        self.scorp_dragon.draw(canvas)

        self.red_player.draw(canvas)
        self.blue_player.draw(canvas)

        red_x, red_y = self.red_player.getPosition()
        blue_x, blue_y = self.blue_player.getPosition()

        flash_width, flash_height = self.flashlight_texture.get_size()
        half_flash_width, half_flash_height = flash_width * 0.5, flash_height * 0.5

        self.flashlight_mask.fill((0, 0, 0))
        self.flashlight_mask.blit(
            self.flashlight_texture,
            (
                red_x + shared_config.HALF_GRID_CELL_SIZE - half_flash_width,
                red_y + shared_config.HALF_GRID_CELL_SIZE - half_flash_height
            ),
            special_flags=pg.BLEND_RGB_ADD
        )
        self.flashlight_mask.blit(
            self.flashlight_texture,
            (
                blue_x + shared_config.HALF_GRID_CELL_SIZE - half_flash_width,
                blue_y + shared_config.HALF_GRID_CELL_SIZE - half_flash_height
            ),
            special_flags=pg.BLEND_RGB_ADD
        )

        canvas.blit(
            self.flashlight_mask,
            (shared_config.GRID_RENDER_OFFSET_X, shared_config.GRID_RENDER_OFFSET_Y),
            special_flags=pg.BLEND_RGB_MULT
        )

        self.maze_manager.drawShimmers(canvas)

        # TODO: Apply Inverse Flashlight to Shimmers

        # ? UI Rendering

        red_score_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{self.red_player.getScore()}pts",
            False,
            shared_config.UI_RED_TEXT
        ), 90.0)

        red_time_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{int(self.game_time)}s",
            False,
            shared_config.UI_RED_TEXT
        ), 90.0)

        blue_score_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{self.blue_player.getScore()}pts",
            False,
            shared_config.UI_BLUE_TEXT
        ), 270.0)

        blue_time_text: pg.Surface = pg.transform.rotate(self.ui_font.render(
            f"{int(self.game_time)}s",
            False,
            shared_config.UI_BLUE_TEXT
        ), 270.0)

        red_score_width, red_score_height = red_score_text.get_size()
        red_time_width = red_time_text.get_width()
        blue_time_height = blue_time_text.get_height()

        canvas.blit(
            red_score_text,
            (canvas_width - red_score_width - GAME_UI_BUFFER_X, canvas_height - red_score_height - GAME_UI_BUFFER_Y)
        )

        canvas.blit(
            red_time_text,
            (canvas_width - red_time_width - GAME_UI_BUFFER_X, GAME_UI_BUFFER_Y)
        )

        canvas.blit(
            blue_score_text,
            (GAME_UI_BUFFER_X, GAME_UI_BUFFER_Y)
        )

        canvas.blit(
            blue_time_text,
            (GAME_UI_BUFFER_X, canvas_height - blue_time_height - GAME_UI_BUFFER_Y)
        )

    def shouldTransition(self) -> bool:
        return self.game_time <= 0.0