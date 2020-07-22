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


def test_main() -> None:
    result = _cli('--help')

    assert result.exit_code == 0

    result = _cli('--path', '#')

    assert result.exit_code != 0
    assert "Path '#' does not exist." in result.stdout

    result = _cli('--path', 'test')

    assert result.exit_code == 0
