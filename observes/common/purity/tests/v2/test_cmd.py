from purity.v2.cmd import (
    Cmd,
)
import pytest
from tempfile import (
    TemporaryFile,
)
from typing import (
    IO,
)


def _print_msg(msg: str, target: IO[str]) -> Cmd[None]:
    return Cmd.from_cmd(lambda: print(msg, file=target))


def test_use_case_1() -> None:
    with pytest.raises(SystemExit):
        with TemporaryFile("r+") as file:

            def _print(msg: str) -> Cmd[None]:
                return _print_msg(msg, file)

            in_val = Cmd.from_cmd(lambda: 245)
            some = in_val.map(lambda i: i + 1).map(str).bind(_print)
            _print("not called")
            pre = _print("Hello World!")
            try:
                pre.bind(lambda _: some).compute()
            except SystemExit as err:
                file.seek(0)
                assert file.readlines() == ["Hello World!\n", "246\n"]
                raise err
