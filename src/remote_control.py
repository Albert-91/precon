import asyncio
import curses

from devices_handlers.distance_sensor import get_distance_ahead
from devices_handlers.driving_engines import turn_right, turn_left, drive_backward, stop_driving, drive_forward, \
    drive_with_intervals

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


DISTANCE_AHEAD_TO_STOP = 3


async def _handle_driving_forward() -> None:
    if await get_distance_ahead() > DISTANCE_AHEAD_TO_STOP:
        drive_with_intervals(drive_forward)
    else:
        stop_driving()


async def _handle_driving_backward() -> None:
    drive_with_intervals(drive_backward)


async def _handle_turning_left() -> None:
    drive_with_intervals(turn_left)


async def _handle_turning_right() -> None:
    drive_with_intervals(turn_right)


async def steer_vehicle(screen) -> None:
    print("Press key arrows OR 'WSAD' to drive your vehicle")
    print("Press 'q' key quit")
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP or char == ord('w'):
            await _handle_driving_forward()
        elif char == curses.KEY_DOWN or char == ord('s'):
            await _handle_driving_backward()
        elif char == curses.KEY_RIGHT or char == ord('d'):
            await _handle_turning_right()
        elif char == curses.KEY_LEFT or char == ord('a'):
            await _handle_turning_left()


if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(steer_vehicle(screen))
    except KeyboardInterrupt:
        print("Finishing remote control...")
    finally:
        loop.close()
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()
