# Standard library
from typing import (
    Callable,
)

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
from click.testing import CliRunner


def _cli(*args: str) -> Result:
    runner = CliRunner(mix_stderr=False)

    return runner.invoke(dispatch, args)


def test_help() -> None:
    result = _cli('--help')
    assert result.exit_code == 0
    assert 'Usage:' in result.output


def test_dispatch_config_not_found(test_config: Callable[[str], str]) -> None:
    result = _cli('#')
    assert result.exit_code != 0
    assert "File '#' does not exist." in result.stderr, \
        (result.stderr, result.stdout, result.output)


def test_dispatch_correct(test_config: Callable[[str], str]) -> None:
    result = _cli(test_config('correct'))
    assert result.exit_code == 0


def test_dispatch_debug_empty(test_config: Callable[[str], str]) -> None:
    result = _cli('--debug', test_config('empty'))
    assert result.exit_code == 0


def test_dispatch_empty(test_config: Callable[[str], str]) -> None:
    result = _cli(test_config('empty'))
    assert result.exit_code == 0


def test_dispatch_null(test_config: Callable[[str], str]) -> None:
    result = _cli(test_config('null'))
    assert result.exit_code == 0


def test_dispatch_token(test_config: Callable[[str], str]) -> None:
    result = _cli('--token', '123', test_config('correct'))
    assert result.exit_code == 1
