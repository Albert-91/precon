import pytest

from exploring import DirectionInfo, Location
from mapping import Mapper, ObstacleLocation


@pytest.mark.parametrize("direction_info, expected_result", [
    ([DirectionInfo(Location(0, 0), angle=0, distance=10)], [ObstacleLocation(10, 0)]),
    ([DirectionInfo(Location(1, 0), angle=0, distance=10)], [ObstacleLocation(11, 0)]),
])
@pytest.mark.asyncio
async def test_map_locations_from_directions_info(mocker, direction_info, expected_result):
    mocker.patch("mapping.Explorer.gather_directions_info", return_value=direction_info)

    mapper = Mapper()
    await mapper.map_locations()

    assert mapper.obstacles == expected_result
