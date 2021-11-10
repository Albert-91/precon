import curses
from typing import Union, Callable
from unittest.mock import patch, Mock

import pytest
from pytest_mock import MockerFixture

from precon.remote_control import steer_vehicle


@pytest.fixture()
def create_screen() -> Callable[[Union[str, int]], Mock]:
    def inner(key: Union[str, int]) -> Mock:
        with patch("precon.remote_control.curses.initscr") as screen:
            if isinstance(key, str):
                key = ord(key)
            screen.getch = Mock(side_effect=[key, ord("q")])
            return screen

    return inner


@pytest.fixture()
def distance_ahead_to_stop() -> int:
    return 3


@pytest.fixture()
def patch_gpio(mocker: MockerFixture) -> None:
    mocker.patch("precon.remote_control.fake_rpi.RPi.GPIO.output")


@pytest.fixture()
def patch_print(mocker: MockerFixture) -> None:
    mocker.patch("builtins.print")


@pytest.fixture()
def patch_time(mocker: MockerFixture) -> None:
    mocker.patch("precon.devices_handlers.driving_engines.time")


@pytest.mark.parametrize(
    "key, called_function",
    [
        (curses.KEY_DOWN, "drive_backward"),
        ("s", "drive_backward"),
        (curses.KEY_LEFT, "turn_left"),
        ("a", "turn_left"),
        (curses.KEY_RIGHT, "turn_right"),
        ("d", "turn_right"),
    ],
)
@pytest.mark.asyncio
async def test_drive_on_pressed_keys(
    mocker: MockerFixture,
    create_screen: Callable[[Union[str, int]], Mock],
    patch_gpio: None,
    patch_print: None,
    patch_time: None,
    key: Union[int, str],
    called_function: str,
) -> None:
    drive_func = mocker.patch(f"precon.remote_control.{called_function}")
    mocker.patch("precon.remote_control.get_distance", return_value=distance_ahead_to_stop)
    screen = create_screen(key)

    await steer_vehicle(screen)

    drive_func.assert_called_once()


@pytest.mark.parametrize(
    "key",
    [
        curses.KEY_UP,
        "w",
    ],
)
@pytest.mark.asyncio
async def test_drive_forward_on_pressed_keys(
    mocker: MockerFixture,
    create_screen: Callable[[Union[str, int]], Mock],
    patch_gpio: None,
    patch_print: None,
    patch_time: None,
    key: Union[int, str],
    distance_ahead_to_stop: int,
) -> None:
    drive_func = mocker.patch("precon.remote_control.drive_forward")
    distance_allows_to_drive = distance_ahead_to_stop + 1
    mocker.patch("precon.remote_control.get_distance", return_value=distance_allows_to_drive)
    screen = create_screen(key)

    await steer_vehicle(screen)

    drive_func.assert_called_once()


@pytest.mark.parametrize(
    "key",
    [
        curses.KEY_UP,
        "w",
        curses.KEY_DOWN,
        "s",
        curses.KEY_LEFT,
        "a",
        curses.KEY_RIGHT,
        "d",
    ],
)
@pytest.mark.asyncio
async def test_stop_after_each_drive(
    mocker: MockerFixture,
    create_screen: Callable[[Union[str, int]], Mock],
    distance_ahead_to_stop: int,
    patch_gpio: None,
    patch_print: None,
    patch_time: None,
    key: Union[int, str],
) -> None:
    mocker.patch("precon.remote_control.get_distance", return_value=distance_ahead_to_stop + 1)
    stop_func = mocker.patch("precon.devices_handlers.driving_engines.stop_driving")
    screen = create_screen(key)

    await steer_vehicle(screen)

    stop_func.assert_called_once()


@pytest.mark.parametrize(
    "key",
    [
        curses.KEY_UP,
        "w",
    ],
)
@pytest.mark.asyncio
async def test_stop_when_distance_ahead_is_equal_or_less_than_3_and_robot_is_driving_forward(
    mocker: MockerFixture,
    create_screen: Callable[[Union[str, int]], Mock],
    distance_ahead_to_stop: int,
    patch_gpio: None,
    patch_print: None,
    patch_time: None,
    key: Union[int, str],
) -> None:
    drive_func = mocker.patch("precon.remote_control.drive_forward")
    stop_func = mocker.patch("precon.remote_control.stop_driving")
    mocker.patch("precon.remote_control.get_distance", return_value=distance_ahead_to_stop)
    screen = create_screen(key)

    await steer_vehicle(screen)

    stop_func.assert_called_once()
    drive_func.assert_not_called()


@pytest.mark.parametrize(
    "key, called_function",
    [
        (curses.KEY_DOWN, "drive_backward"),
        ("s", "drive_backward"),
        (curses.KEY_LEFT, "turn_left"),
        ("a", "turn_left"),
        (curses.KEY_RIGHT, "turn_right"),
        ("d", "turn_right"),
    ],
)
@pytest.mark.asyncio
async def test_not_stop_when_distance_ahead_is_equal_or_less_than_3(
    mocker: MockerFixture,
    create_screen: Callable[[Union[str, int]], Mock],
    distance_ahead_to_stop: int,
    patch_gpio: None,
    patch_print: None,
    patch_time: None,
    key: Union[int, str],
    called_function: str,
) -> None:
    drive_func = mocker.patch(f"precon.remote_control.{called_function}")
    mocker.patch("precon.remote_control.get_distance", return_value=distance_ahead_to_stop)
    screen = create_screen(key)

    await steer_vehicle(screen)

    drive_func.assert_called_once()
