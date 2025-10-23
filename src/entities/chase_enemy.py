import pygame as pg

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
        self.FRAME_TIME: float = frame_time
        self.animation_frames: list[pg.Surface] = animation_frames

    def reset(self) -> None:
        self.position_x, self.position_y = self.start_position
        
        self.animation_index = 0
        self.animation_time = 0.0

    def update(self, delta_time: float) -> None:
        self.animation_time += delta_time
        if self.animation_time >= self.FRAME_TIME:
            self.animation_time -= self.FRAME_TIME
            self.animation_index = (self.animation_index + 1) % len(self.animation_frames)

    def draw(self, canvas: pg.Surface) -> None:
        canvas.blit(
            pg.transform.rotate(
                self.animation_frames[self.animation_index],
                self.rotation
            ),
            (self.position_x, self.position_y)
        )