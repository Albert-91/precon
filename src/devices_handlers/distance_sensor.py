import time

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO


GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
TRIGGER_PIN = 21
ECHO_PIN = 20

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def _initilize_sensor():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)


def _get_echo_time(signal_level: bool):
    while GPIO.input(ECHO_PIN) == signal_level:
        pulse_time = time.time()
    return pulse_time


def _compute_distance(signal_delay):
    # divider for uS to s
    const_divider = 1000000 / 58
    return signal_delay * const_divider


def handle_distance_sensor() -> int:
    _initilize_sensor()
    pulse_start, pulse_end = _get_echo_time(False), _get_echo_time(True)
    signal_delay = pulse_end - pulse_start
    distance = _compute_distance(signal_delay)
    return int(distance)
