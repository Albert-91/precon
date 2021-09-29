from exploring import Localizer


def test_updating_current_location():
    localizator = Localizer(x=0, y=0, angle=0)

    localizator.update(x=1, y=0, angle=0)

    assert localizator.current_location == (1, 0)
    assert localizator.current_angle == 0


def test_updating_current_angle():
    localizator = Localizer(x=0, y=0, angle=0)

    localizator.update(x=0, y=0, angle=10)

    assert localizator.current_location == (0, 0)
    assert localizator.current_angle == 10


def test_all_locations_with_updated_x():
    localizator = Localizer(x=0, y=0)

    localizator.update(1, 0)

    assert len(localizator.all_locations) == 2
    assert localizator.all_locations[0] == (0, 0)
    assert localizator.all_locations[1] == (1, 0)
    assert localizator.all_locations[-1] == localizator.current_location


def test_all_locations_with_updated_x_multiple_times():
    localizator = Localizer(x=0, y=0)
    UPDATES_NUMBER = 5

    for i in range(UPDATES_NUMBER):
        localizator.update(i, 0)

    assert len(localizator.all_locations) == UPDATES_NUMBER + 1
    assert localizator.all_locations[-1] == localizator.current_location
    x = 0
    for i in range(UPDATES_NUMBER):
        assert localizator.all_locations[i] == (x, 0)
        x += i


def test_all_locations_with_updated_y_multiple_times():
    localizator = Localizer(x=0, y=0)
    UPDATES_NUMBER = 5

    for i in range(UPDATES_NUMBER):
        localizator.update(0, i)

    assert len(localizator.all_locations) == UPDATES_NUMBER + 1
    assert localizator.all_locations[-1] == localizator.current_location
    y = 0
    for i in range(UPDATES_NUMBER):
        assert localizator.all_locations[i] == (0, y)
        y += i
