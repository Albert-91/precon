from unittest.mock import Mock

import pytest

from exploring import Explorer, Location, DirectionInfo, NoDirectionFound


@pytest.mark.asyncio
async def test_find_direction_to_move(mocker):
    expected_direction = DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), distance=10)
    directions = [DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), i) for i in range(5)]
    directions.append(expected_direction)
    mocker.patch("exploring.Explorer.gather_directions_info", return_value=directions)

    explorer = Explorer()
    direction = await explorer.get_direction_to_move()

    assert direction == expected_direction


@pytest.mark.asyncio
async def test_find_direction_to_move_with_gathered_empty_list(mocker):
    mocker.patch("exploring.Explorer.gather_directions_info", return_value=[])

    explorer = Explorer()

    with pytest.raises(NoDirectionFound):
        await explorer.get_direction_to_move()


@pytest.mark.asyncio
async def test_quantity_of_gathered_directions_info(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")

    explorer = Explorer()
    directions = await explorer.gather_directions_info(directions_number=10)

    assert len(directions) == 11


@pytest.mark.asyncio
async def test_types_of_gathered_directions_info(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")

    explorer = Explorer()
    directions = await explorer.gather_directions_info(directions_number=10)

    for direction in directions:
        assert isinstance(direction, DirectionInfo)


@pytest.mark.asyncio
async def test_number_of_measured_distances_during_gathering_directions_info(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    get_distance_function = mocker.patch("exploring.get_distance_ahead")

    explorer = Explorer()
    await explorer.gather_directions_info(directions_number=10)

    assert get_distance_function.call_count == 11


@pytest.mark.asyncio
async def test_values_of_measured_distances_during_gathering_directions_info(mocker):
    NUMBER_OF_DIRECTIONS_TO_CHECK = 10
    measured_distance = range(NUMBER_OF_DIRECTIONS_TO_CHECK+1)
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead", side_effect=measured_distance)

    explorer = Explorer()
    directions = await explorer.gather_directions_info(directions_number=NUMBER_OF_DIRECTIONS_TO_CHECK)

    for direction, val in zip(directions, measured_distance):
        assert direction.distance == val


@pytest.mark.asyncio
async def test_gather_directions_info_number_of_turning_to_measure_distance(mocker):
    turning_right_func = mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")
    DIRECTIONS_NUMBER = 10
    angle_to_rotate = int(360 / 10)

    explorer = Explorer()
    await explorer.gather_directions_info(directions_number=DIRECTIONS_NUMBER)

    assert turning_right_func.call_count == 11
    for call in turning_right_func.mock_calls:
        call.assert_any_call(angle_to_rotate)


@pytest.mark.asyncio
async def test_gather_directions_info_last_of_angles_is_less_than_360(mocker):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")

    explorer = Explorer()
    directions = await explorer.gather_directions_info(directions_number=10)

    assert directions[-1].angle <= 360


@pytest.mark.asyncio
async def test_gather_directions_info_always_fill_to_360_degrees(mocker):
    turning_right_func = mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")

    explorer = Explorer()
    directions = await explorer.gather_directions_info(directions_number=11)
    angle_to_do_360 = 360 - directions[-1].angle

    turning_right_func.assert_called_with(angle_to_do_360)


@pytest.mark.parametrize("directions_number", [
    0,
    500,
    -50,
    1.1,
    None,
    "",
    "50",
])
@pytest.mark.asyncio
async def test_gather_directions_info_bad_input(mocker, directions_number):
    mocker.patch("exploring.turn_right_on_angle")
    mocker.patch("exploring.get_distance_ahead")

    explorer = Explorer()

    with pytest.raises(ValueError):
        await explorer.gather_directions_info(directions_number=directions_number)
