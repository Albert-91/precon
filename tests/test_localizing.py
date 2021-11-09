from precon.exploring import Localizer


def test_updating_current_location() -> None:
    localizator = Localizer(x=0, y=0, angle=0)

    localizator.update(movement=1, angle=0)

    assert localizator.current_location == (0, 1.0)
    assert localizator.current_angle == 0


def test_updating_current_angle() -> None:
    localizator = Localizer(x=0, y=0, angle=0)

    localizator.update(movement=0, angle=10)

    assert localizator.current_location == (0, 0)
    assert localizator.current_angle == 10


def test_computing_location_with_angle_grater_than_0() -> None:
    localizator = Localizer(x=0, y=0, angle=0)

    localizator.update(movement=1, angle=45)

    assert localizator.current_location == (0.707, 0.707)
    assert localizator.current_angle == 45


def test_all_locations_with_updated_x() -> None:
    localizator = Localizer(x=0, y=0)

    localizator.update(1, 0)

    assert len(localizator.all_locations) == 2
    assert localizator.all_locations[0] == (0, 0)
    assert localizator.all_locations[1] == (0, 1.0)
    assert localizator.all_locations[-1] == localizator.current_location


def test_all_locations_with_updated_x_multiple_times() -> None:
    localizator = Localizer(x=0, y=0)
    UPDATES_NUMBER = 5

    for i in range(UPDATES_NUMBER):
        localizator.update(i, 0)

    assert len(localizator.all_locations) == UPDATES_NUMBER + 1
    assert localizator.all_locations[-1] == localizator.current_location
    x = 0
    for i in range(UPDATES_NUMBER):
        assert localizator.all_locations[i] == (0, x)
        x += i
