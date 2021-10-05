import logging
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple
import math

from devices_handlers.distance_sensor import get_distance_ahead
from devices_handlers.driving_engines import turn_right_on_angle, drive_forward_on_units, drive_backward_on_units

logger = logging.getLogger(__name__)


DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK = 10


@dataclass(frozen=True)
class Location:
    x: float
    y: float


@dataclass(frozen=True)
class DirectionInfo:
    location: Location
    angle: int
    distance: int


@dataclass(frozen=True)
class ObstacleLocation:
    x: int
    y: int


@dataclass(frozen=True)
class UndiscoveredRegion:
    x: float
    y: float


class Localizer:

    def __init__(self, x: float = 0, y: float = 0, angle: int = 0) -> None:
        self._x = x
        self._y = y
        self._angle = angle
        self._locations: List = [self.current_location]

    @property
    def current_location(self) -> Tuple[float, float]:
        return self._x, self._y

    @property
    def current_angle(self) -> int:
        return self._angle

    @property
    def all_locations(self) -> List[Tuple[int, int]]:
        return self._locations

    def update(self, movement, angle=0) -> None:
        self._y = round(self._y + movement * math.cos(math.radians(angle)), 3)
        self._x = round(self._x + movement * math.sin(math.radians(angle)), 3)
        self._angle += angle
        logger.debug(f"Set x = {self._x}, y = {self._y}, angle={self._angle}")
        self._locations.append(self.current_location)


class Mapper:
    """Mapper keeps all mapped locations."""

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
            logger.debug(f"Added new obstacle's location: {location}")

    @staticmethod
    def _compute_obstacle_coordinates(direction: DirectionInfo) -> ObstacleLocation:
        def round_half_up(n: float, decimals: int = 0) -> float:
            multiplier = 10 ** decimals
            return math.floor(n * multiplier + 0.5) / multiplier

        y = direction.location.y + direction.distance * math.cos(math.radians(direction.angle))
        x = direction.location.x + direction.distance * math.sin(math.radians(direction.angle))
        return ObstacleLocation(int(round_half_up(x)), int(round_half_up(y)))


class PathPlanner:

    def __init__(self, mapper: Mapper) -> None:
        self._mapper: Mapper = mapper
        self._undiscovered_regions: List[UndiscoveredRegion] = []

    @property
    def undiscovered_regions(self) -> List[UndiscoveredRegion]:
        return self._undiscovered_regions

    async def compute_undiscovered_location(self) -> None:
        def count_neighbours_in_radius(point: ObstacleLocation, nodes: List[ObstacleLocation], radius: int = 2) -> int:
            result = []
            for node in nodes:
                if (point.x - node.x) ** 2 + (point.y - node.y) ** 2 <= radius and not point == node:
                    result.append(node)
            return len(result)

        for location in self._mapper.obstacles:
            neighbours_number = count_neighbours_in_radius(location, self._mapper.obstacles)
            if neighbours_number < 2:
                self._undiscovered_regions.append(UndiscoveredRegion(location.x, location.y))


class Explorer:
    """Explorer knows current location and takes information which areas has to be discovered.
    He decides which area will be discovered as first."""

    MAXIMUM_NUMBER_OF_DIRECTIONS = 20

    def __init__(self, localizer) -> None:
        self._localizer = localizer
        self._mapper = Mapper()

    async def run(self):
        await self.scan_area()
        while not self._mapper.obstacles:
            self.move_forward(unit=100)
            await self.scan_area()

    async def scan_area(self, directions_number: int = DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK) -> List[DirectionInfo]:
        self._validate_directions_number(directions_number)
        angle_per_rotation = int(360 / directions_number)
        angle = self._localizer.current_angle
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

    def move_forward(self, unit: int = 1) -> None:
        drive_forward_on_units(unit=unit)
        self._localizer.update(unit)

    def move_backward(self, unit: int = 1) -> None:
        drive_backward_on_units(unit=unit)
        self._localizer.update(-unit)

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
