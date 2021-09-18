import time

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
TRIGGER_PIN = 12
ECHO_PIN = 16

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def _initilize_sensor() -> None:
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)


def _get_echo_time(signal_level: bool) -> float:
    pulse_time = 0.0
    while GPIO.input(ECHO_PIN) == signal_level:
        pulse_time = time.time()
    return pulse_time


def _compute_distance(signal_delay: float) -> float:
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    return (signal_delay * 34300) / 2


def get_distance_ahead() -> int:
    """Function returns distance in `cm`"""

    _initilize_sensor()
    pulse_start, pulse_end = _get_echo_time(False), _get_echo_time(True)
    signal_delay = pulse_end - pulse_start
    distance = _compute_distance(signal_delay)
    return int(distance)


if __name__ == '__main__':
    try:
        while True:
            dist = get_distance_ahead()
            print(dist)
            time.sleep(1)
    finally:
        GPIO.cleanup()
