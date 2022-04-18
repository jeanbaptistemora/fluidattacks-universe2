# pylint: disable=unused-argument

from typing import (
    Any,
)

# constants
GROUP = "continuoustest"
GROUP_BAD = "does-not-exist"


def test_resources_1(relocate: Any, cli_runner: Any) -> None:
    result = cli_runner(f"utils --does-subs-exist {GROUP}".split())
    assert result.exit_code == 0


def test_resources_3(relocate: Any, cli_runner: Any) -> None:
    result = cli_runner(f"resources --read-dev {GROUP}".split())
    assert result.exit_code == 0
