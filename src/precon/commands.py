import asyncio
import curses

import click

from precon.devices_handlers.distance_sensor import show_distance as show_distance_func
from precon.remote_control import steer_vehicle

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


@click.command(name="rc")
def remote_control() -> None:
    screen = curses.initscr()
    screen.keypad(True)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(steer_vehicle(screen))
    except KeyboardInterrupt:
        print("Finishing remote control...")
    finally:
        screen.keypad(False)
        curses.endwin()
        GPIO.cleanup()


@click.command(name="show-distance")
def show_distance() -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(show_distance_func())
    except KeyboardInterrupt:
        print("Finishing measuring distance...")
    finally:
        GPIO.cleanup()
