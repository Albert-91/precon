from unittest.mock import Mock, PropertyMock

import pytest

from exploring import Explorer, Location, DirectionInfo, NoDirectionFound, Mapper, Localizer


@pytest.mark.asyncio
async def test_find_direction_to_move(mocker):
    expected_direction = DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), distance=10)
    directions = [DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), i) for i in range(5)]
    directions.append(expected_direction)
    mocker.patch("exploring.Explorer.scan_area", return_value=directions)

    localizer = Localizer()
    explorer = Explorer(localizer)
    direction = await explorer.get_direction_to_move()

    assert direction == expected_direction


@pytest.mark.asyncio
async def test_find_direction_to_move_with_gathered_empty_list(mocker):
    mocker.patch("exploring.Explorer.scan_area", return_value=[])

    localizer = Localizer()
    explorer = Explorer(localizer)

    with pytest.raises(NoDirectionFound):
        await explorer.get_direction_to_move()


@pytest.mark.asyncio
async def test_quantity_of_gathered_directions_info(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=10)

    assert len(directions) == 11


@pytest.mark.asyncio
async def test_types_of_gathered_directions_info(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=10)

    for direction in directions:
        assert isinstance(direction, DirectionInfo)


@pytest.mark.asyncio
async def test_number_of_measured_distances_during_gathering_directions_info(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    get_distance_function = mocker.patch("exploring.get_distance_ahead", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    await explorer.scan_area(directions_number=10)

    assert get_distance_function.call_count == 11


@pytest.mark.asyncio
async def test_values_of_measured_distances_during_gathering_directions_info(mocker):
    NUMBER_OF_DIRECTIONS_TO_CHECK = 10
    measured_distance = range(NUMBER_OF_DIRECTIONS_TO_CHECK+1)
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", side_effect=measured_distance)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=NUMBER_OF_DIRECTIONS_TO_CHECK)

    for direction, val in zip(directions, measured_distance):
        assert direction.distance == val


@pytest.mark.asyncio
async def test_scan_area_number_of_turning_to_measure_distance(mocker):
    turning_right_func = mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", return_value=1)
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
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=10)

    assert directions[-1].angle <= 360


@pytest.mark.asyncio
async def test_scan_area_always_fill_to_360_degrees(mocker):
    turning_right_func = mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", return_value=1)

    localizer = Localizer()
    explorer = Explorer(localizer)
    directions = await explorer.scan_area(directions_number=11)
    angle_to_do_360 = 360 - directions[-1].angle

    turning_right_func.assert_called_with(angle_to_do_360)


@pytest.mark.asyncio
async def test_scan_area_map_all_directions(mocker):
    map_obstacles_method = mocker.patch("exploring.Mapper.map_obstacles")
    mocker.patch("exploring.get_distance_ahead", return_value=1)

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
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")

    localizer = Localizer()
    explorer = Explorer(localizer)
    with pytest.raises(ValueError):
        await explorer.scan_area(directions_number=directions_number)


@pytest.mark.asyncio
async def test_scan_area_set_direction_number_grater_than_maximum(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")
    MAXIMUM_NUMBER_OF_DIRECTIONS = 10
    mocker.patch.object(Explorer, "MAXIMUM_NUMBER_OF_DIRECTIONS", return_value=MAXIMUM_NUMBER_OF_DIRECTIONS, new_callable=PropertyMock)

    localizer = Localizer()
    explorer = Explorer(localizer)
    with pytest.raises(ValueError):
        await explorer.scan_area(directions_number=MAXIMUM_NUMBER_OF_DIRECTIONS + 1)


@pytest.mark.asyncio
async def test_explore_undiscovered_area__scan_area_when_there_is_no_mapped_obstacles(mocker):
    mocker.patch.object(Mapper, "obstacles", return_value=[], new_callable=PropertyMock)
    scan_area_method = mocker.patch("exploring.Explorer.scan_area")

    localizer = Localizer()
    explorer = Explorer(localizer)
    await explorer.explore_undiscovered_area()

    scan_area_method.assert_called()


@pytest.mark.asyncio
async def test_moving_forward_and_updating_location():
    localizer = Localizer()
    explorer = Explorer(localizer)
    explorer.move_forward(unit=1)

    assert localizer.current_location == (0, 1)


@pytest.mark.asyncio
async def test_moving_backward_and_updating_location():
    localizer = Localizer()
    explorer = Explorer(localizer)
    explorer.move_backward(unit=1)

    assert localizer.current_location == (0, -1)
