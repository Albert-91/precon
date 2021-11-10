import curses

from precon.devices_handlers.distance_sensor import get_distance
from precon.devices_handlers.driving_engines import turn_right, turn_left, drive_backward, stop_driving, drive_forward

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi

    GPIO = fake_rpi.RPi.GPIO


DISTANCE_AHEAD_TO_STOP = 3


async def _handle_driving_forward() -> None:
    if await get_distance() > DISTANCE_AHEAD_TO_STOP:
        drive_forward()
    else:
        stop_driving()


async def _handle_driving_backward() -> None:
    drive_backward()


async def _handle_turning_left() -> None:
    turn_left()


async def _handle_turning_right() -> None:
    turn_right()


class Screen:
    def __init__(self):
        self.screen = None

    def __enter__(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.screen.keypad(False)
        curses.endwin()

    def get_pressed_char(self):
        if not self.screen:
            raise ValueError("Screen is not initialized. Use it by context manager.")
        return self.screen.getch()


async def steer_vehicle(screen) -> None:
    print("Press key arrows OR 'WSAD' to drive your vehicle")
    print("Press 'q' key quit")

    with screen:
        while True:
            char = screen.get_pressed_char()
            if char == ord("q"):
                break
            handlers = {
                curses.KEY_UP: _handle_driving_forward,
                ord("w"): _handle_driving_forward,
                curses.KEY_DOWN: _handle_driving_backward,
                ord("s"): _handle_driving_backward,
                curses.KEY_LEFT: _handle_turning_left,
                ord("a"): _handle_turning_left,
                curses.KEY_RIGHT: _handle_turning_right,
                ord("d"): _handle_turning_right,
            }
            driving_handler = handlers.get(char)

            if driving_handler:
                await driving_handler()
