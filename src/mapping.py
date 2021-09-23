from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple


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


class Mapper:

    def __init__(self) -> None:
        self._localizer = Localizer()

    async def gather_directions_info(self) -> List[DirectionInfo]:
        pass

    async def get_direction_to_move(self) -> DirectionInfo:
        directions = await self.gather_directions_info()
        if not directions:
            raise NoDirectionFound
        return reduce(lambda a, b: a if a.distance > b.distance else b, directions)


class NoDirectionFound(Exception):
    pass
