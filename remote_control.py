import curses
import RPi.GPIO as GPIO


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
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            drive_forward()
        elif char == curses.KEY_DOWN:
            drive_backward()
        elif char == curses.KEY_RIGHT:
            turn_right()
        elif char == curses.KEY_LEFT:
            turn_left()
        elif char == 10:
            stop()


if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    try:
        steer()
    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()
