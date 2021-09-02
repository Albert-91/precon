import curses
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

# main drives pins
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)


def drive_forward():
    GPIO.output(7, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(15, True)


def drive_backward():
    GPIO.output(7, True)
    GPIO.output(11, False)
    GPIO.output(13, True)
    GPIO.output(15, False)


def turn_right():
    GPIO.output(7, True)
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(15, True)


def turn_left():
    GPIO.output(7, False)
    GPIO.output(11, True)
    GPIO.output(13, True)
    GPIO.output(15, False)


def stop():
    GPIO.output(7, False)
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(15, False)


def steer():
    try:
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
    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()


if __name__ == '__main__':
    steer()
