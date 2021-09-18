from devices_handlers.distance_sensor import get_distance_ahead


def test_getting_distance_for_one_second_of_signal_delay(mocker):
    mocker.patch("devices_handlers.distance_sensor.time.time", side_effect=[1, 2])
    mocker.patch("devices_handlers.distance_sensor.fake_rpi.RPi.GPIO.input", side_effect=[False, True, True, False])
    # for one second it should be integer from half of 34300 (sonic speed) -> 17150 cm
    expected_result = 17150

    distance = get_distance_ahead()

    assert distance == expected_result
