from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple
import math


from devices_handlers.distance_sensor import get_distance_ahead
from devices_handlers.driving_engines import turn_right_on_angle


DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK = 10


@dataclass(frozen=True)
class Location:
    x: int
    y: int


@dataclass(frozen=True)
class DirectionInfo:
    location: Location
    angle: int
    distance: int


@dataclass(frozen=True)
class ObstacleLocation:
    x: int
    y: int


class Localizer:

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self._x = x
        self._y = y
        self._locations: List = [self.current_location]

    @property
    def current_location(self) -> Tuple[int, int]:
        return self._x, self._y

    @property
    def all_locations(self) -> List[Tuple[int, int]]:
        return self._locations

    def update(self, x, y) -> None:
        self._x += x
        self._y += y
        self._locations.append(self.current_location)


class Mapper:
    """Mapper keeps all mapped locations and knows which areas are undiscovered."""

    MAXIMUM_DISTANCE_TO_SET_OBSTACLE = 2000

    def __init__(self):
        self._obstacles: List[ObstacleLocation] = []

    @property
    def obstacles(self) -> List[ObstacleLocation]:
        return self._obstacles

    async def map_obstacles(self, directions: List[DirectionInfo]) -> None:
        directions = filter(lambda x: x.distance <= self.MAXIMUM_DISTANCE_TO_SET_OBSTACLE, directions)
        for direction in directions:
            location = self._compute_obstacle_coordinates(direction)
            self._obstacles.append(location)

    @staticmethod
    def _compute_obstacle_coordinates(direction: DirectionInfo) -> ObstacleLocation:
        def round_half_up(n: float, decimals: int = 0) -> float:
            multiplier = 10 ** decimals
            return math.floor(n * multiplier + 0.5) / multiplier

        y = direction.location.y + direction.distance * math.cos(math.radians(direction.angle))
        x = direction.location.x + direction.distance * math.sin(math.radians(direction.angle))
        return ObstacleLocation(int(round_half_up(x)), int(round_half_up(y)))


class Explorer:
    """Explorer knows current location and takes information which areas has to be discovered.
    He decides which area will be discovered as first."""

    MAXIMUM_NUMBER_OF_DIRECTIONS = 20

    def __init__(self) -> None:
        self._localizer = Localizer()
        self._mapper = Mapper()

    async def explore_undiscovered_area(self):
        if not self._mapper.obstacles:
            await self.scan_area()

    async def scan_area(self, directions_number: int = DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK) -> List[DirectionInfo]:
        self._validate_directions_number(directions_number)
        angle_per_rotation = int(360 / directions_number)
        angle = 0
        directions = [
            DirectionInfo(
                location=Location(*self._localizer.current_location),
                angle=angle,
                distance=await get_distance_ahead()
            )
        ]
        for _ in range(directions_number):
            angle += angle_per_rotation
            directions.append(
                DirectionInfo(
                    location=Location(*self._localizer.current_location),
                    angle=angle,
                    distance=await get_distance_ahead()
                )
            )
            turn_right_on_angle(angle_per_rotation)
        turn_right_on_angle(360 - angle)
        await self._mapper.map_obstacles(directions)
        return directions

    async def get_direction_to_move(self) -> DirectionInfo:
        directions = await self.scan_area()
        if not directions:
            raise NoDirectionFound
        return reduce(lambda a, b: a if a.distance > b.distance else b, directions)

    def _validate_directions_number(self, directions_number) -> None:
        if not isinstance(directions_number, int) \
            or directions_number <= 1 \
            or directions_number > self.MAXIMUM_NUMBER_OF_DIRECTIONS:
            raise ValueError


class NoDirectionFound(Exception):
    pass
