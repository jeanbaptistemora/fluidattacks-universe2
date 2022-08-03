from fa_purity import (
    Cmd,
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
    TextIO,
)


def text_buffer(text: TextIO) -> Stream[str]:
    def _is_closed() -> Cmd[bool]:
        return Cmd.from_cmd(lambda: text.buffer.closed)

    def _iter_lines() -> Iterable[str]:
        with TextIOWrapper(text.buffer, encoding="utf-8") as file:
            line = file.readline()
            while line:
                yield line
                line = file.readline()

    iterable = _is_closed().map(lambda b: _iter_lines() if b else iter([]))
    return unsafe_from_cmd(iterable)


def stdin_buffer() -> Stream[str]:
    return text_buffer(sys.stdin)
