import pytest


@pytest.mark.asyncio
async def test_find_farhest_direction():

    localizator = Localizator()
    current_location = localizator.get_current_location()
    explorer = Explorer(current_location)
    # explorer.get_directions()
    explorer.get_d()
