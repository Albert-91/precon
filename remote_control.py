import RPi.GPIO as GPIO
import keyboard


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


def steer():
    print("Press key arrows OR 'WSAD' to drive your vehicle")
    print("Press 'q' key quit")
    while True:
        if keyboard.is_pressed('q'):
            break
        elif keyboard.is_pressed('w') or keyboard.is_pressed(keyboard.KEY_UP):
            drive_forward()
        elif keyboard.is_pressed('s') or keyboard.is_pressed(keyboard.KEY_DOWN):
            drive_backward()
        elif keyboard.is_pressed('a') or keyboard.is_pressed("left"):
            turn_left()
        elif keyboard.is_pressed('d') or keyboard.is_pressed("right"):
            turn_right()
        else:
            stop()


if __name__ == '__main__':
    try:
        steer()
    finally:
        GPIO.cleanup()
