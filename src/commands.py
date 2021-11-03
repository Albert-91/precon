import asyncio
import curses

import click

from devices_handlers.distance_sensor import show_distance as show_distance_func
from remote_control import steer_vehicle

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


@click.command(name="rc")
def remote_control():
    screen = curses.initscr()
    screen.keypad(True)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(steer_vehicle(screen))
    except KeyboardInterrupt:
        print("Finishing remote control...")
    finally:
        loop.close()
        screen.keypad(False)
        curses.endwin()
        GPIO.cleanup()
