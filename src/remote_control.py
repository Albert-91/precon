import curses
import time
from typing import Callable

from devices_handlers.distance_sensor import get_distance_ahead

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


GPIO.setmode(GPIO.BOARD)

RIGHT_ENGINE_FORWARD_PIN_IDX = 7
RIGHT_ENGINE_BACKWARD_PIN_IDX = 11
LEFT_ENGINE_FORWARD_PIN_IDX = 13
LEFT_ENGINE_BACKWARD_PIN_IDX = 15

GPIO.setup(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.OUT)
GPIO.setup(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.OUT)
GPIO.setup(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.OUT)
GPIO.setup(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.OUT)


def drive_right_engine_forward() -> None:
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.HIGH)


def drive_right_engine_backward() -> None:
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.HIGH)


def drive_left_engine_forward() -> None:
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.HIGH)


def drive_left_engine_backward() -> None:
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.HIGH)


def drive_forward() -> None:
    drive_left_engine_forward()
    drive_right_engine_forward()


def drive_backward() -> None:
    drive_left_engine_backward()
    drive_right_engine_backward()


def turn_right() -> None:
    drive_left_engine_forward()
    drive_right_engine_backward()


def turn_left() -> None:
    drive_left_engine_backward()
    drive_right_engine_forward()


def stop_driving() -> None:
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)


def drive_on_pressed_button(drive_callback: Callable) -> None:
    drive_callback()
    time.sleep(0.1)
    stop_driving()


def steer_vehicle(screen) -> None:
    print("Press key arrows OR 'WSAD' to drive your vehicle")
    print("Press 'q' key quit")
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP or char == ord('w'):
            drive_on_pressed_button(drive_forward)
        elif char == curses.KEY_DOWN or char == ord('s'):
            drive_on_pressed_button(drive_backward)
        elif char == curses.KEY_RIGHT or char == ord('d'):
            drive_on_pressed_button(turn_right)
        elif char == curses.KEY_LEFT or char == ord('a'):
            drive_on_pressed_button(turn_left)


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
