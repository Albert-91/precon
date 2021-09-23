from mapping import Localizer


def test_updating_current_location():
    localizator = Localizer(x=0, y=0)

    localizator.update(1, 0)

    assert localizator.current_location == (1, 0)


def test_all_locations():
    localizator = Localizer(x=0, y=0)

    localizator.update(1, 0)

    assert len(localizator.all_locations) == 2
    assert localizator.all_locations[0] == (0, 0)
    assert localizator.all_locations[1] == (1, 0)
    assert localizator.all_locations[-1] == localizator.current_location
