from unittest.mock import Mock, PropertyMock

import pytest

from precon.exploring import Explorer, Location, DirectionInfo, NoDirectionFound, Mapper, Localizer, ObstacleLocation


@pytest.mark.asyncio
async def test_find_direction_to_move(mocker):
    expected_direction = DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), distance=10)
    directions = [DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), i) for i in range(5)]
    directions.append(expected_direction)
    mocker.patch("precon.exploring.Explorer.scan_area", return_value=directions)

    localizer = Localizer()
    explorer = Explorer(localizer)
    direction = await explorer.get_direction_to_move()

    assert direction == expected_direction


@pytest.mark.asyncio
async def test_find_direction_to_move_with_gathered_empty_list(mocker):
    mocker.patch("precon.exploring.Explorer.scan_area", return_value=[])

    localizer = Localizer()
    explorer = Explorer(localizer)

    with pytest.raises(NoDirectionFound):
        await explorer.get_direction_to_move()


@pytest.mark.asyncio
async def test_quantity_of_gathered_directions_info(mocker):
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=10)

    assert len(directions) == 11


@pytest.mark.asyncio
async def test_types_of_gathered_directions_info(mocker):
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=10)

    for direction in directions:
        assert isinstance(direction, DirectionInfo)


@pytest.mark.asyncio
async def test_number_of_measured_distances_during_gathering_directions_info(mocker):
    mocker.patch("precon.exploring.turn_right_on_angle")
    get_distance_function = mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    await explorer.scan_area(directions_number=10)

    assert get_distance_function.call_count == 11


@pytest.mark.asyncio
async def test_values_of_measured_distances_during_gathering_directions_info(mocker):
    NUMBER_OF_DIRECTIONS_TO_CHECK = 10
    measured_distance = range(NUMBER_OF_DIRECTIONS_TO_CHECK+1)
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", side_effect=measured_distance)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=NUMBER_OF_DIRECTIONS_TO_CHECK)

    for direction, val in zip(directions, measured_distance):
        assert direction.distance == val


@pytest.mark.asyncio
async def test_scan_area_number_of_turning_to_measure_distance(mocker):
    turning_right_func = mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", return_value=1)
    DIRECTIONS_NUMBER = 10
    angle_to_rotate = int(360 / 10)

    localizer = Localizer()
    explorer = Explorer(localizer)
    await explorer.scan_area(directions_number=DIRECTIONS_NUMBER)

    assert turning_right_func.call_count == 11
    for call in turning_right_func.mock_calls:
        call.assert_any_call(angle_to_rotate)


@pytest.mark.asyncio
async def test_scan_area_last_of_angles_is_less_than_360(mocker):
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=10)

    assert directions[-1].angle <= 360


@pytest.mark.asyncio
async def test_scan_area__saved_angles_are_relative_to_current_angle(mocker):
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer(angle=10)
    explorer = Explorer(localizer)
    assert localizer.current_angle == 10
    directions = await explorer.scan_area(directions_number=2)

    assert directions[0].angle == 10
    assert directions[1].angle == 190
    assert directions[2].angle == 370


@pytest.mark.asyncio
async def test_scan_area_always_fill_to_360_degrees(mocker):
    turning_right_func = mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=11)
    angle_to_do_360 = 360 - directions[-1].angle

    turning_right_func.assert_called_with(angle_to_do_360)


@pytest.mark.asyncio
async def test_scan_area_map_all_directions(mocker):
    map_obstacles_method = mocker.patch("precon.exploring.Mapper.map_obstacles")
    mocker.patch("precon.exploring.get_distance", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=11)

    map_obstacles_method.assert_called_once_with(directions)


@pytest.mark.parametrize("directions_number", [
    0,
    -50,
    1.1,
    None,
    "",
    "50",
])
@pytest.mark.asyncio
async def test_scan_area_bad_input(mocker, directions_number):
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance")

    localizer = Localizer()
    explorer = Explorer(localizer)
    with pytest.raises(ValueError):
        await explorer.scan_area(directions_number=directions_number)


@pytest.mark.asyncio
async def test_scan_area_set_direction_number_grater_than_maximum(mocker):
    mocker.patch("precon.exploring.turn_right_on_angle")
    mocker.patch("precon.exploring.get_distance")
    MAXIMUM_NUMBER_OF_DIRECTIONS = 10
    mocker.patch.object(Explorer, "MAXIMUM_NUMBER_OF_DIRECTIONS", return_value=MAXIMUM_NUMBER_OF_DIRECTIONS, new_callable=PropertyMock)

    localizer = Localizer()
    explorer = Explorer(localizer)
    with pytest.raises(ValueError):
        await explorer.scan_area(directions_number=MAXIMUM_NUMBER_OF_DIRECTIONS + 1)


@pytest.mark.asyncio
async def test_explore_undiscovered_area__scan_area_when_there_is_no_mapped_obstacles(mocker):
    mocker.patch.object(Mapper, "obstacles",
                        side_effect=[[], [], [ObstacleLocation(Mock(), Mock())]], new_callable=PropertyMock)
    scan_area_method = mocker.patch("precon.exploring.Explorer.scan_area")

    localizer = Localizer()
    explorer = Explorer(localizer)
    await explorer.run()

    assert scan_area_method.call_count == 3


@pytest.mark.asyncio
async def test_explore_undiscovered_area__with_already_scanned_obstacles(mocker):
    mocker.patch.object(Mapper, "obstacles",
                        return_value=[ObstacleLocation(Mock(), Mock())], new_callable=PropertyMock)
    scan_area_method = mocker.patch("precon.exploring.Explorer.scan_area")

    localizer = Localizer()
    explorer = Explorer(localizer)
    await explorer.run()

    scan_area_method.assert_called_once()


def test_moving_forward_and_updating_location():
    localizer = Localizer()
    explorer = Explorer(localizer)
    explorer.move_forward(unit=1)

    assert localizer.current_location == (0, 1)


def test_moving_backward_and_updating_location():
    localizer = Localizer()
    explorer = Explorer(localizer)
    explorer.move_backward(unit=1)

    assert localizer.current_location == (0, -1)
