# standar libraries
import os

# Third party libraries
import pytest
from click.testing import CliRunner

# Local libraries
from forces.cli import main


def test_cli_strict(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ['--token', test_token, '--strict', '--repo-name', 'forces'])
    assert result.exit_code == 1


def test_cli_lax(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ['--token', test_token, '--lax', '--repo-path', '../'])
    assert result.exit_code == 0


def test_cli_invalid_group(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ['--token', test_token, '--lax', '--repo-path', '../'])
    assert result.exit_code == 0


def test_cli_out_to_file(test_token: str) -> None:
    runner = CliRunner()
    runner.invoke(main, [
        '--token', test_token, '--strict', '--output', 'test.yml',
        '--repo-path', '../'
    ])
    assert os.path.exists(f'{os.getcwd()}/test.yml') == True
