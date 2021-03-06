from typing import List
from unittest.mock import PropertyMock

import pytest
from pytest_mock import MockerFixture

from precon.exploring import DirectionInfo, Location, Mapper, ObstacleLocation


@pytest.mark.parametrize(
    "direction_info, expected_result",
    [
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
    ],
)
@pytest.mark.asyncio
async def test_map_locations_from_directions_info(
    mocker: MockerFixture, direction_info: List[DirectionInfo], expected_result: List[ObstacleLocation]
) -> None:
    mocker.patch.object(Mapper, "MAXIMUM_DISTANCE_TO_SET_OBSTACLE", return_value=50, new_callable=PropertyMock)

    mapper = Mapper()
    await mapper.map_obstacles(direction_info)

    assert mapper.obstacles == expected_result


@pytest.mark.asyncio
async def test_map_locations_exclude_distances_which_sensor_does_not_handle(mocker: MockerFixture) -> None:
    MAXIMUM_DISTANCE_TO_SET_OBSTACLE = 50
    mocker.patch.object(
        Mapper,
        "MAXIMUM_DISTANCE_TO_SET_OBSTACLE",
        return_value=MAXIMUM_DISTANCE_TO_SET_OBSTACLE,
        new_callable=PropertyMock,
    )
    direction_info = [
        DirectionInfo(Location(0, 0), angle=0, distance=MAXIMUM_DISTANCE_TO_SET_OBSTACLE - 1),
        DirectionInfo(Location(0, 0), angle=0, distance=MAXIMUM_DISTANCE_TO_SET_OBSTACLE),
        DirectionInfo(Location(0, 0), angle=0, distance=MAXIMUM_DISTANCE_TO_SET_OBSTACLE + 1),
        DirectionInfo(Location(0, 0), angle=0, distance=MAXIMUM_DISTANCE_TO_SET_OBSTACLE * 2),
    ]
    expected_result = [
        ObstacleLocation(0, MAXIMUM_DISTANCE_TO_SET_OBSTACLE - 1),
        ObstacleLocation(0, MAXIMUM_DISTANCE_TO_SET_OBSTACLE),
    ]

    mapper = Mapper()
    await mapper.map_obstacles(direction_info)

    assert len(mapper.obstacles) == 2
    assert mapper.obstacles == expected_result
