import math
from dataclasses import dataclass
from typing import List

from exploring import Explorer, DirectionInfo

DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK = 10


@dataclass(frozen=True)
class ObstacleLocation:
    x: int
    y: int


class Mapper:
    """Mapper keeps all mapped locations and knows which areas are undiscovered."""

    MAXIMUM_DISTANCE_TO_SET_OBSTACLE = 2000

    def __init__(self):
        self._obstacles: List[ObstacleLocation] = []
        self._explorer = Explorer()

    @property
    def obstacles(self) -> List[ObstacleLocation]:
        return self._obstacles

    async def map_obstacles(self) -> None:
        directions = await self._explorer.gather_directions_info(DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK)
        directions = filter(lambda x: x.distance <= self.MAXIMUM_DISTANCE_TO_SET_OBSTACLE, directions)
        for direction in directions:
            location = self._compute_obstacle_coordinates(direction)
            self._obstacles.append(location)

    @staticmethod
    def _compute_obstacle_coordinates(direction: DirectionInfo) -> ObstacleLocation:
        def round_half_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.floor(n * multiplier + 0.5) / multiplier

        y = direction.location.y + direction.distance * math.cos(math.radians(direction.angle))
        x = direction.location.x + direction.distance * math.sin(math.radians(direction.angle))
        return ObstacleLocation(round_half_up(x), round_half_up(y))
