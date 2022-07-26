from fa_purity import (
    Cmd,
    Maybe,
    ResultE,
    Stream,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from io import (
    TextIOWrapper,
)
import sys
from typing import (
    Iterable,
)


class CannotReopenStdinBuffer(Exception):
    pass


def stdin_buffer() -> Cmd[ResultE[Stream[str]]]:
    def _iter_lines() -> Iterable[str]:
        with TextIOWrapper(sys.stdin.buffer, encoding="utf-8") as file:
            line = file.readline()
            while line:
                yield line
                line = file.readline()

    def _is_closed() -> Cmd[bool]:
        return Cmd.from_cmd(lambda: sys.stdin.buffer.closed)

    stream = unsafe_from_cmd(Cmd.from_cmd(lambda: iter(_iter_lines())))
    return _is_closed().map(
        lambda b: Maybe.from_optional(stream if not b else None)
        .to_result()
        .alt(lambda _: CannotReopenStdinBuffer())
    )
