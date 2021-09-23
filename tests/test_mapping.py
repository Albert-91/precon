from unittest.mock import Mock

import pytest

from mapping import Mapper, Location, DirectionInfo


@pytest.mark.asyncio
async def test_find_direction_to_move(mocker):
    expected_direction = DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), distance=10)
    directions = [DirectionInfo(Location(Mock(int), Mock(int)), Mock(int), i) for i in range(5)]
    directions.append(expected_direction)
    mocker.patch("mapping.Mapper.gather_directions_info", return_value=directions)

    mapper = Mapper()
    direction = await mapper.get_direction_to_move()

    assert direction == expected_direction
