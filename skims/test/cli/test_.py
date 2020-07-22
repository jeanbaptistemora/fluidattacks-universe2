# Third party libraries
from click.testing import (
    CliRunner,
    Result,
)

# Local libraries
from cli import (
    dispatch,
)

# Third parties libraries
import pytest
from click.testing import CliRunner


def _cli(*args: str) -> Result:
    runner = CliRunner()

    return runner.invoke(dispatch, args)


def test_help() -> None:
    result = _cli('--help')
    assert result.exit_code == 0
    assert 'Usage:' in result.output

    result = _cli('run', '--help')
    assert result.exit_code == 0
    assert 'Usage:' in result.output

    result = _cli('sync', '--help')
    assert result.exit_code == 0
    assert 'Usage:' in result.output


def test_dispatch() -> None:
    result = _cli('--debug')
    assert result.exit_code == 2
    assert 'Error: Missing command.' in result.output


def test_dispatch_run() -> None:
    result = _cli('run', '--path', '#')
    assert result.exit_code != 0
    assert "Path '#' does not exist." in result.output

    result = _cli('--debug', 'run', '--path', 'test')
    assert result.exit_code == 0


def test_dispatch_sync(test_group: str) -> None:
    result = _cli('sync')
    assert result.exit_code == 1
    assert 'Option: --group is mandatory.' in result.output

    result = _cli('sync', '--group', test_group)
    assert result.exit_code == 0
