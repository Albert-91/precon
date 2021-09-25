from dataclasses import dataclass
from typing import List

from exploring import Explorer, DirectionInfo

DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK = 10


@dataclass(frozen=True)
class ObstacleLocation:
    x: int
    y: int


class Mapper:

    def __init__(self):
        self._obstacles: List[ObstacleLocation] = []
        self._explorer = Explorer()

    @property
    def obstacles(self) -> List[ObstacleLocation]:
        return self._obstacles

    async def map_locations(self) -> None:
        directions = await self._explorer.gather_directions_info(DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK)
        for direction in directions:
            location = await self._compute_obstacle_coordinates(direction)
            self._obstacles.append(location)

    @staticmethod
    async def _compute_obstacle_coordinates(direction: DirectionInfo) -> ObstacleLocation:
        x = direction.location.x + direction.distance
        return ObstacleLocation(x, 0)
