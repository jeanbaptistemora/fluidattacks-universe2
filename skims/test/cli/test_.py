# Third party libraries
from click.testing import (
    CliRunner,
    Result,
)

# Local libraries
from cli import (
    main,
)

# Third parties libraries
import pytest
from click.testing import CliRunner


def _cli(*args: str) -> Result:
    runner = CliRunner()

    return runner.invoke(main, args)


def test_main() -> None:
    result = _cli('--help')

    assert result.exit_code == 0
