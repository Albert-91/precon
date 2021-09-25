from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple

from devices_handlers.distance_sensor import get_distance_ahead
from devices_handlers.driving_engines import turn_right_on_angle


DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK = 10
MAXIMUM_NUMBER_OF_DIRECTIONS = 20


@dataclass(frozen=True)
class Location:
    x: int
    y: int


@dataclass(frozen=True)
class DirectionInfo:
    location: Location
    angle: int
    distance: int


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


class Explorer:

    def __init__(self) -> None:
        self._localizer = Localizer()

    async def gather_directions_info(self, directions_number: int) -> List[DirectionInfo]:
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
        return directions

    async def get_direction_to_move(self) -> DirectionInfo:
        directions = await self.gather_directions_info(DEFAULT_NUMBER_OF_DIRECTIONS_TO_CHECK)
        if not directions:
            raise NoDirectionFound
        return reduce(lambda a, b: a if a.distance > b.distance else b, directions)

    def _validate_directions_number(self, directions_number) -> None:
        if not isinstance(directions_number, int) \
            or directions_number <= 1 \
            or directions_number > MAXIMUM_NUMBER_OF_DIRECTIONS:
            raise ValueError


class NoDirectionFound(Exception):
    pass
