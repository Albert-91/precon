import time

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


GPIO.setmode(GPIO.BOARD)
TRIGGER_PIN_IDX = 12
ECHO_PIN_IDX = 16

GPIO.setup(TRIGGER_PIN_IDX, GPIO.OUT)
GPIO.setup(ECHO_PIN_IDX, GPIO.IN)


def _initialize_sensor() -> None:
    GPIO.output(TRIGGER_PIN_IDX, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN_IDX, False)


def _get_echo_time(signal_level: bool) -> float:
    pulse_time = 0.0
    start_time = time.time()
    while GPIO.input(ECHO_PIN_IDX) == signal_level:
        pulse_time = time.time()
        # protection before not coming echo
        if time.time() - start_time > 2:
            return pulse_time
    return pulse_time


def _compute_distance(signal_delay: float) -> float:
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    return (signal_delay * 34300) / 2


def get_distance_ahead() -> int:
    """Function returns distance in `cm`"""

    _initialize_sensor()
    pulse_start, pulse_end = _get_echo_time(False), _get_echo_time(True)
    signal_delay = pulse_end - pulse_start
    distance = _compute_distance(signal_delay)
    return int(distance)


if __name__ == '__main__':
    try:
        while True:
            dist = get_distance_ahead()
            print(dist, "cm")
            time.sleep(1)
    finally:
        GPIO.cleanup()
