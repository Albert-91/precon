import time
from typing import Callable

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


def _drive_right_engine_forward() -> None:
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.HIGH)


def _drive_right_engine_backward() -> None:
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.HIGH)


def _drive_left_engine_forward() -> None:
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.HIGH)


def _drive_left_engine_backward() -> None:
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.HIGH)


def drive_with_intervals(drive_callback: Callable[[], None], movement_time: float = 0.1) -> Callable[[], None]:
    def inner() -> None:
        drive_callback()
        time.sleep(movement_time)
        stop_driving()
    return inner


@drive_with_intervals
def drive_forward() -> None:
    _drive_left_engine_forward()
    _drive_right_engine_forward()


@drive_with_intervals
def drive_backward() -> None:
    _drive_left_engine_backward()
    _drive_right_engine_backward()


@drive_with_intervals
def turn_right() -> None:
    _drive_left_engine_backward()
    _drive_right_engine_forward()


@drive_with_intervals
def turn_left() -> None:
    _drive_left_engine_forward()
    _drive_right_engine_backward()


def stop_driving() -> None:
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.LOW)
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.LOW)


def turn_right_on_angle(angle: float) -> None:
    pass


def turn_left_on_angle(angle: float) -> None:
    pass


def drive_forward_on_units(unit: int = 1) -> None:
    pass


def drive_backward_on_units(unit: int = 1) -> None:
    pass
