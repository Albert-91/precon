import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from precon.commands import remote_control, show_distance


@pytest.fixture()
def cli_runner() -> CliRunner:
    return CliRunner()


def test_remote_control_run_steering_vehicle(mocker: MockerFixture, cli_runner: CliRunner) -> None:
    mocker.patch("precon.commands.curses.initscr")
    mocker.patch("precon.commands.curses.endwin")
    steer_vehicle = mocker.patch("precon.commands.steer_vehicle")

    result = cli_runner.invoke(remote_control)

    assert result.exit_code == 0
    steer_vehicle.assert_called_once()


def test_get_distance_ahead_of_sensor(mocker: MockerFixture, cli_runner: CliRunner) -> None:
    show_distance_func = mocker.patch("precon.commands.show_distance_func")

    result = cli_runner.invoke(show_distance)

    assert result.exit_code == 0
    show_distance_func.assert_called_once()
