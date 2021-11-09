import pytest
from pytest_mock import MockerFixture

from precon.devices_handlers.distance_sensor import get_distance


@pytest.mark.asyncio
async def test_getting_distance_for_one_second_of_signal_delay(mocker: MockerFixture) -> None:
    mocker.patch("precon.devices_handlers.distance_sensor.time.time", side_effect=[1, 1, 1, 1, 2, 1])
    mocker.patch("precon.devices_handlers.distance_sensor.fake_rpi.RPi.GPIO.input",
                 side_effect=[False, True, True, False])
    # for one second it should be integer from half of 34300 (sonic speed) -> 17150 cm
    expected_result = 17150

    distance = await get_distance()

    assert distance == expected_result


@pytest.mark.asyncio
async def test_getting_distance_for_one_second_of_signal_delay_with_not_coming_echo(mocker: MockerFixture) -> None:
    mocker.patch("precon.devices_handlers.distance_sensor.time.time", side_effect=[0, 1, 3, 0, 2, 3])
    mocker.patch("precon.devices_handlers.distance_sensor.fake_rpi.RPi.GPIO.input", side_effect=[False, True])
    # for one second it should be integer from half of 34300 (sonic speed) -> 17150 cm
    expected_result = 17150

    distance = await get_distance()

    assert distance == expected_result
