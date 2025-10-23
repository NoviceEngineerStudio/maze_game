import math
import heapq
from typing import Any, Generator
from ..scenes import shared_config

RAD_2_DEG: float = 180.0 / math.pi

def performAStar(
    initial_position: tuple[int, int],
    target_position: tuple[int, int],
    maze: list[list[bool]]
) -> list[tuple[int, int]]:
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(x: int, y: int) -> Generator[tuple[int, int], Any, None]:
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < shared_config.GRID_COLUMN_COUNT and 0 <= ny < shared_config.GRID_ROW_COUNT and not maze[nx][ny]:
                yield (nx, ny)

    open_set: list[tuple[int, int, tuple[int, int]]] = []
    heapq.heappush(open_set, (heuristic(initial_position, target_position), 0, initial_position))

    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: dict[tuple[int, int], int] = { initial_position: 0 }

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current == target_position:
            path: list[tuple[int, int]] = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in neighbors(*current):
            tentative_g = current_g + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, target_position)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return []
