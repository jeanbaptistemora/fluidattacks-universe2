# standar libraries
import os

# Third party libraries
import pytest
from click.testing import CliRunner

# Local libraries
from forces.cli import main


def test_cli_strict(test_token: str, test_group: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ['--token', test_token, '--group', test_group, '--strict'])
    assert result.exit_code == 1


def test_cli_lax(test_token: str, test_group: str) -> None:
    runner = CliRunner()
    result = runner.invoke(main,
                           ['--token', test_token, '--group', test_group, '--lax'])
    assert result.exit_code == 0


def test_cli_invalid_token(test_group: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ['--token', 'invalid_token', '--group', test_group, '--lax'])
    assert result.exit_code == 2


def test_cli_invalid_group(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ['--token', test_token, '--group', 'invalid_group', '--lax'])
    assert result.exit_code == 1


def test_cli_out_to_file(test_token: str, test_group: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ['--token', test_token, '--group', test_group, '--strict', '--output', 'test.yml'])
    assert os.path.exists(f'{os.getcwd()}/test.yml') == True
