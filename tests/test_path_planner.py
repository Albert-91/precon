from unittest.mock import PropertyMock

import pytest
from pytest_mock import MockerFixture

from precon.exploring import PathPlanner, ObstacleLocation, UndiscoveredRegion, Mapper


@pytest.mark.asyncio
async def test_computing_undiscovered_locations_with_line_from_obstacles_locations(mocker: MockerFixture) -> None:
    obstacles = [
        ObstacleLocation(x=0, y=0),
        ObstacleLocation(x=1, y=0),
        ObstacleLocation(x=2, y=0),
        ObstacleLocation(x=3, y=0),
    ]
    mocker.patch.object(Mapper, "obstacles", new_callable=PropertyMock, return_value=obstacles)

    path_planner = PathPlanner(Mapper())
    await path_planner.compute_undiscovered_location()

    assert path_planner.undiscovered_regions == [
        UndiscoveredRegion(x=0, y=0),
        UndiscoveredRegion(x=3, y=0),
    ]


@pytest.mark.asyncio
async def test_computing_undiscovered_locations_with_two_crossed_lines_from_obstacles_locations(
    mocker: MockerFixture
) -> None:
    obstacles = [
        ObstacleLocation(x=0, y=3),
        ObstacleLocation(x=0, y=2),
        ObstacleLocation(x=0, y=1),
        ObstacleLocation(x=0, y=0),
        ObstacleLocation(x=1, y=0),
        ObstacleLocation(x=2, y=0),
        ObstacleLocation(x=3, y=0),
    ]
    mocker.patch.object(Mapper, "obstacles", new_callable=PropertyMock, return_value=obstacles)

    path_planner = PathPlanner(Mapper())
    await path_planner.compute_undiscovered_location()

    assert path_planner.undiscovered_regions == [
        UndiscoveredRegion(x=0, y=3),
        UndiscoveredRegion(x=3, y=0),
    ]
