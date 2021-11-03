import pytest
from click.testing import CliRunner

from commands import remote_control, show_distance


@pytest.fixture()
def cli_runner():
    return CliRunner()


def test_remote_control_run_steering_vehicle(mocker, cli_runner):
    mocker.patch("commands.curses.initscr")
    mocker.patch("commands.curses.endwin")
    steer_vehicle = mocker.patch("commands.steer_vehicle")

    result = cli_runner.invoke(remote_control)

    assert result.exit_code == 0
    steer_vehicle.assert_called_once()
