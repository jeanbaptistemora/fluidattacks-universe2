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
    runner = CliRunner(mix_stderr=False)

    return runner.invoke(dispatch, args)


def test_help() -> None:
    result = _cli('--help')
    assert result.exit_code == 0
    assert 'Usage:' in result.output


def test_dispatch(test_group: str) -> None:
    result = _cli('--debug')
    assert result.exit_code == 0

    result = _cli('--path', '#')
    assert result.exit_code != 0
    assert "Path '#' does not exist" in result.stderr, \
        (result.stderr, result.stdout, result.output)

    result = _cli('--path', 'test')
    assert result.exit_code == 0

    result = _cli('--group', test_group, '--path', 'test')
    assert result.exit_code == 0
