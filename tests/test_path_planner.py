from unittest.mock import PropertyMock

from exploring import PathPlanner, ObstacleLocation, UndiscoveredRegion, Mapper


def test_computing_undiscovered_locations_with_line_from_obstacles_locations(mocker):
    obstacles = [
        ObstacleLocation(x=0, y=0),
        ObstacleLocation(x=1, y=0),
        ObstacleLocation(x=2, y=0),
        ObstacleLocation(x=3, y=0),
    ]
    mocker.patch.object(Mapper, "obstacles", new_callable=PropertyMock, return_value=obstacles)

    path_planner = PathPlanner()
    path_planner.compute_undiscovered_location()

    assert path_planner.undiscovered_regions == [
        UndiscoveredRegion(x=0, y=0),
        UndiscoveredRegion(x=3, y=0),
    ]
