import RPi.GPIO as GPIO
from pynput.keyboard import Key, Listener


GPIO.setmode(GPIO.BOARD)

RIGHT_ENGINE_FORWARD_PIN_IDX = 7
RIGHT_ENGINE_BACKWARD_PIN_IDX = 11
LEFT_ENGINE_FORWARD_PIN_IDX = 13
LEFT_ENGINE_BACKWARD_PIN_IDX = 15

GPIO.setup(RIGHT_ENGINE_FORWARD_PIN_IDX, GPIO.OUT)
GPIO.setup(RIGHT_ENGINE_BACKWARD_PIN_IDX, GPIO.OUT)
GPIO.setup(LEFT_ENGINE_FORWARD_PIN_IDX, GPIO.OUT)
GPIO.setup(LEFT_ENGINE_BACKWARD_PIN_IDX, GPIO.OUT)


def drive_right_engine_forward():
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, False)
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, True)


def drive_right_engine_backward():
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, False)
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, True)


def drive_left_engine_forward():
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, False)
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, True)


def drive_left_engine_backward():
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, False)
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, True)


def drive_forward():
    drive_left_engine_forward()
    drive_right_engine_forward()


def drive_backward():
    drive_left_engine_backward()
    drive_right_engine_backward()


def turn_right():
    drive_left_engine_forward()
    drive_right_engine_backward()


def turn_left():
    drive_left_engine_backward()
    drive_right_engine_forward()


def stop():
    GPIO.output(RIGHT_ENGINE_FORWARD_PIN_IDX, False)
    GPIO.output(RIGHT_ENGINE_BACKWARD_PIN_IDX, False)
    GPIO.output(LEFT_ENGINE_FORWARD_PIN_IDX, False)
    GPIO.output(LEFT_ENGINE_BACKWARD_PIN_IDX, False)


class QuitListener(Exception):
    pass


def steer():
    def on_press(key):
        if key.char == 'q':
            raise QuitListener
        action_to_press = {
            Key.up: drive_forward,
            Key.down: drive_backward,
            Key.right: turn_right,
            Key.left: turn_left
        }
        action = action_to_press.get(key)
        if action:
            action()

    def on_release(key):
        if key in [Key.up, Key.down, Key.left, Key.right]:
            stop()

    print("Press key arrows to drive your vehicle")
    print("Press 'q' key quit")
    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()


if __name__ == '__main__':
    try:
        steer()
    except QuitListener:
        print("Quitting from steering...")
    finally:
        GPIO.cleanup()
