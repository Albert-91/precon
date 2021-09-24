from unittest.mock import Mock

import pytest

from mapping import Mapper, Location, DirectionInfo, NoDirectionFound


@pytest.mark.asyncio
async def test_find_direction_to_move(mocker):
    expected_direction = DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), distance=10)
    directions = [DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), i) for i in range(5)]
    directions.append(expected_direction)
    mocker.patch("mapping.Mapper.gather_directions_info", return_value=directions)

    mapper = Mapper()
    direction = await mapper.get_direction_to_move()

    assert direction == expected_direction


@pytest.mark.asyncio
async def test_find_direction_to_move_with_gathered_empty_list(mocker):
    mocker.patch("mapping.Mapper.gather_directions_info", return_value=[])

    mapper = Mapper()

    with pytest.raises(NoDirectionFound):
        await mapper.get_direction_to_move()


@pytest.mark.asyncio
async def test_quantity_of_gathered_directions_info(mocker):
    mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead")

    mapper = Mapper()
    directions = await mapper.gather_directions_info(directions_number=10)

    assert len(directions) == 10


@pytest.mark.asyncio
async def test_types_of_gathered_directions_info(mocker):
    mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead")

    mapper = Mapper()
    directions = await mapper.gather_directions_info(directions_number=10)

    for direction in directions:
        assert isinstance(direction, DirectionInfo)


@pytest.mark.asyncio
async def test_number_of_measured_distances_during_gathering_directions_info(mocker):
    mocker.patch("mapping.turn_right_on_angle")
    get_distance_function = mocker.patch("mapping.get_distance_ahead")

    mapper = Mapper()
    await mapper.gather_directions_info(directions_number=10)

    assert get_distance_function.call_count == 10


@pytest.mark.asyncio
async def test_values_of_measured_distances_during_gathering_directions_info(mocker):
    NUMBER_OF_DIRECTIONS_TO_CHECK = 10
    MEASURED_DISTANCES = range(NUMBER_OF_DIRECTIONS_TO_CHECK)
    mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead", side_effect=MEASURED_DISTANCES)

    mapper = Mapper()
    directions = await mapper.gather_directions_info(directions_number=NUMBER_OF_DIRECTIONS_TO_CHECK)

    for direction, val in zip(directions, MEASURED_DISTANCES):
        assert direction.distance == val


@pytest.mark.asyncio
async def test_gather_directions_info_number_of_turning_to_measure_distance(mocker):
    turning_right_func = mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead")
    DIRECTIONS_NUMBER = 10
    angle_to_rotate = int(360 / 10)

    mapper = Mapper()
    await mapper.gather_directions_info(directions_number=DIRECTIONS_NUMBER)

    assert turning_right_func.call_count == 11
    for call in turning_right_func.mock_calls:
        call.assert_any_call(angle_to_rotate)


@pytest.mark.asyncio
async def test_gather_directions_info_last_of_angles_is_less_than_360(mocker):
    mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead")

    mapper = Mapper()
    directions = await mapper.gather_directions_info(directions_number=10)

    assert directions[-1].angle <= 360


@pytest.mark.asyncio
async def test_gather_directions_info_always_do_360_degrees(mocker):
    turning_right_func = mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead")

    mapper = Mapper()
    directions = await mapper.gather_directions_info(directions_number=11)
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
    mocker.patch("mapping.turn_right_on_angle")
    mocker.patch("mapping.get_distance_ahead")

    mapper = Mapper()

    with pytest.raises(ValueError):
        await mapper.gather_directions_info(directions_number=directions_number)