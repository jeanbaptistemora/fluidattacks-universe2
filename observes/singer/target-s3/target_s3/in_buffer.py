# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from io import (
    TextIOWrapper,
)
import logging
import sys
from typing import (
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


def stdin_buffer() -> Stream[str]:
    return text_buffer(sys.stdin)
