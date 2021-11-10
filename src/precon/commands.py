import asyncio

import click

from precon.devices_handlers.distance_sensor import show_distance as show_distance_func
from precon.remote_control import steer_vehicle, Screen

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi

    GPIO = fake_rpi.RPi.GPIO


@click.command(name="rc")
def remote_control() -> None:
    loop = asyncio.get_event_loop()
    try:
        with Screen() as screen:
            loop.run_until_complete(steer_vehicle(screen))
    except KeyboardInterrupt:
        print("Finishing remote control...")
    except Exception as e:
        print("Raised unexpected error: %s" % e)
    finally:
        GPIO.cleanup()


@click.command(name="show-distance")
def show_distance() -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(show_distance_func())
    except KeyboardInterrupt:
        print("Finishing measuring distance...")
    except Exception as e:
        print("Raised unexpected error: %s" % e)
    finally:
        GPIO.cleanup()
