from click.testing import CliRunner
from commands import remote_control


def test_remote_control_run_steering_vehicle(mocker):
    mocker.patch("commands.curses.initscr")
    mocker.patch("commands.curses.endwin")
    steer_vehicle = mocker.patch("commands.steer_vehicle")
    runner = CliRunner()

    result = runner.invoke(remote_control)

    assert result.exit_code == 0
    steer_vehicle.assert_called_once()
