from . import (
    _utils,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from fa_purity.stream.transform import (
    squash,
)
from io import (
    TextIOWrapper,
)
import logging
import sys
from typing import (
    IO,
    Iterable,
    TextIO,
)

LOG = logging.getLogger(__name__)


def text_buffer(text: TextIO) -> Stream[str]:
    def _is_closed() -> Cmd[bool]:
        return Cmd.from_cmd(lambda: text.buffer.closed).bind(
            lambda b: _utils.log_cmd(
                lambda: LOG.warning("%s file is closed!", text.name), b
            )
            if b
            else _utils.log_cmd(lambda: None, b)
        )

    def _iter_lines() -> Iterable[str]:
        with TextIOWrapper(text.buffer, encoding="utf-8") as file:
            line = file.readline()
            while line:
                yield line
                line = file.readline()

    iterable = _is_closed().map(lambda b: iter([]) if b else _iter_lines())
    return unsafe_from_cmd(iterable)


def _emit(target: TextIO, line: str) -> Cmd[None]:
    def _action() -> None:
        target.write(line)

    return Cmd.from_cmd(_action)


def process_buffer(
    input_io: TextIO, output_io: TextIO, bypass_input: bool
) -> Stream[str]:
    return (
        text_buffer(input_io)
        .map(
            lambda i: _emit(output_io, i).map(lambda _: i)
            if bypass_input
            else Cmd.from_cmd(lambda: i)
        )
        .transform(lambda s: squash(s))
    )


def stdin_buffer(bypass_input: bool) -> Stream[str]:
    return process_buffer(sys.stdin, sys.stdout, bypass_input)
