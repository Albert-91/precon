import curses
import time
from typing import Callable

from devices_handlers.distance_sensor import get_distance_ahead
from devices_handlers.driving_engines import turn_right, turn_left, drive_backward, stop_driving, drive_forward

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


DISTANCE_AHEAD_TO_STOP = 3


def _drive_on_pressed_button(drive_callback: Callable) -> None:
    drive_callback()
    time.sleep(0.1)
    stop_driving()


def _handle_driving_forward() -> None:
    if get_distance_ahead() > DISTANCE_AHEAD_TO_STOP:
        _drive_on_pressed_button(drive_forward)
    else:
        stop_driving()


def _handle_driving_backward() -> None:
    _drive_on_pressed_button(drive_backward)


def _handle_turning_left() -> None:
    _drive_on_pressed_button(turn_left)


def _handle_turning_right() -> None:
    _drive_on_pressed_button(turn_right)


def steer_vehicle(screen) -> None:
    print("Press key arrows OR 'WSAD' to drive your vehicle")
    print("Press 'q' key quit")
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP or char == ord('w'):
            _handle_driving_forward()
        elif char == curses.KEY_DOWN or char == ord('s'):
            _handle_driving_backward()
        elif char == curses.KEY_RIGHT or char == ord('d'):
            _handle_turning_right()
        elif char == curses.KEY_LEFT or char == ord('a'):
            _handle_turning_left()


if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    try:
        steer_vehicle(screen)
    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()
