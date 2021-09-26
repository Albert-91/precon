import pytest

from exploring import DirectionInfo, Location
from mapping import Mapper, ObstacleLocation


@pytest.mark.parametrize("direction_info, expected_result", [
    ([DirectionInfo(Location(0, 0), angle=0, distance=10)], [ObstacleLocation(0, 10)]),
    ([DirectionInfo(Location(1, 0), angle=0, distance=10)], [ObstacleLocation(1, 10)]),
    ([DirectionInfo(Location(0, 1), angle=0, distance=10)], [ObstacleLocation(0, 11)]),

    ([DirectionInfo(Location(0, 0), angle=30, distance=10)], [ObstacleLocation(5, 9)]),
    ([DirectionInfo(Location(0, 0), angle=45, distance=10)], [ObstacleLocation(7, 7)]),
    ([DirectionInfo(Location(0, 0), angle=60, distance=10)], [ObstacleLocation(9, 5)]),

    ([DirectionInfo(Location(1, 1), angle=30, distance=10)], [ObstacleLocation(6, 10)]),
    ([DirectionInfo(Location(1, 1), angle=45, distance=10)], [ObstacleLocation(8, 8)]),
    ([DirectionInfo(Location(1, 1), angle=60, distance=10)], [ObstacleLocation(10, 6)]),

    ([DirectionInfo(Location(-1, -1), angle=30, distance=10)], [ObstacleLocation(4, 8)]),
    ([DirectionInfo(Location(-1, -1), angle=45, distance=10)], [ObstacleLocation(6, 6)]),
    ([DirectionInfo(Location(-1, -1), angle=60, distance=10)], [ObstacleLocation(8, 4)]),
])
@pytest.mark.asyncio
async def test_map_locations_from_directions_info(mocker, direction_info, expected_result):
    mocker.patch("mapping.Explorer.gather_directions_info", return_value=direction_info)

    mapper = Mapper()
    await mapper.map_locations()

    assert mapper.obstacles == expected_result
