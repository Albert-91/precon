import pytest

from precon.devices_handlers.driving_engines import drive_forward, drive_backward, turn_right, turn_left, stop_driving


@pytest.fixture
def right_engine_forward_pin():
    return 7


@pytest.fixture
def right_engine_backward_pin():
    return 11


@pytest.fixture
def left_engine_forward_pin():
    return 13


@pytest.fixture
def left_engine_backward_pin():
    return 15


@pytest.fixture()
def patch_time(mocker):
    mocker.patch("precon.devices_handlers.driving_engines.time")


def test_driving_forward(
    mocker,
    right_engine_forward_pin,
    right_engine_backward_pin,
    left_engine_forward_pin,
    left_engine_backward_pin,
    patch_time
):
    output = mocker.patch("precon.devices_handlers.driving_engines.fake_rpi.RPi.GPIO.output")

    drive_forward()

    output.assert_any_call(right_engine_forward_pin, True)
    output.assert_any_call(left_engine_forward_pin, True)
    output.assert_any_call(right_engine_backward_pin, False)
    output.assert_any_call(left_engine_backward_pin, False)


def test_driving_backward(
    mocker,
    right_engine_forward_pin,
    right_engine_backward_pin,
    left_engine_forward_pin,
    left_engine_backward_pin,
    patch_time
):
    output = mocker.patch("precon.devices_handlers.driving_engines.fake_rpi.RPi.GPIO.output")

    drive_backward()

    output.assert_any_call(right_engine_forward_pin, False)
    output.assert_any_call(left_engine_forward_pin, False)
    output.assert_any_call(right_engine_backward_pin, True)
    output.assert_any_call(left_engine_backward_pin, True)


def test_turning_right(
    mocker,
    right_engine_forward_pin,
    right_engine_backward_pin,
    left_engine_forward_pin,
    left_engine_backward_pin,
    patch_time
):
    output = mocker.patch("precon.devices_handlers.driving_engines.fake_rpi.RPi.GPIO.output")

    turn_right()

    output.assert_any_call(right_engine_forward_pin, True)
    output.assert_any_call(left_engine_forward_pin, False)
    output.assert_any_call(right_engine_backward_pin, False)
    output.assert_any_call(left_engine_backward_pin, True)


def test_turning_left(
    mocker,
    right_engine_forward_pin,
    right_engine_backward_pin,
    left_engine_forward_pin,
    left_engine_backward_pin,
    patch_time
):
    output = mocker.patch("precon.devices_handlers.driving_engines.fake_rpi.RPi.GPIO.output")

    turn_left()

    output.assert_any_call(right_engine_forward_pin, False)
    output.assert_any_call(left_engine_forward_pin, True)
    output.assert_any_call(right_engine_backward_pin, True)
    output.assert_any_call(left_engine_backward_pin, False)


def test_stop_drives(
    mocker,
    right_engine_forward_pin,
    right_engine_backward_pin,
    left_engine_forward_pin,
    left_engine_backward_pin,
    patch_time
):
    output = mocker.patch("precon.devices_handlers.driving_engines.fake_rpi.RPi.GPIO.output")

    stop_driving()

    output.assert_any_call(right_engine_forward_pin, False)
    output.assert_any_call(left_engine_forward_pin, False)
    output.assert_any_call(right_engine_backward_pin, False)
    output.assert_any_call(left_engine_backward_pin, False)
