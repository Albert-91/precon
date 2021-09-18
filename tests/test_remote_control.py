import curses
from unittest.mock import patch, Mock

import pytest

from remote_control import steer_vehicle


@pytest.fixture()
def create_screen():
    def inner(key):
        with patch("remote_control.curses.initscr") as screen:
            if isinstance(key, str):
                key = ord(key)
            screen.getch = Mock(side_effect=[key, ord('q')])
            return screen
    return inner


@pytest.mark.parametrize('key, called_function', [
    (curses.KEY_UP, "drive_forward"),
    ("w", "drive_forward"),
    (curses.KEY_DOWN, "drive_backward"),
    ("s", "drive_backward"),
    (curses.KEY_LEFT, "turn_left"),
    ("a", "turn_left"),
    (curses.KEY_RIGHT, "turn_right"),
    ("d", "turn_right"),
])
def test_drive_on_pressed_keys(mocker, create_screen, key, called_function):
    drive_func = mocker.patch(f"remote_control.{called_function}")
    screen = create_screen(key)

    steer_vehicle(screen)

    drive_func.assert_called_once()


@pytest.mark.parametrize('key', [
    curses.KEY_UP, "w",
    curses.KEY_DOWN, "s",
    curses.KEY_LEFT, "a",
    curses.KEY_RIGHT, "d",
])
def test_stop_after_each_drive(mocker, create_screen, key):
    stop_func = mocker.patch("remote_control.stop_driving")
    screen = create_screen(key)

    steer_vehicle(screen)

    stop_func.assert_called_once()
