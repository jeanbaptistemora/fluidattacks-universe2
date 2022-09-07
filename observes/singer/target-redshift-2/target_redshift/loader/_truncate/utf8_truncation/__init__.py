# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .core import (
    new_primary_byte,
    PrimaryByte,
    secondary_bytes_of,
)
from fa_purity import (
    Maybe,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from typing import (
    Tuple,
)


class NotFound(Exception):
    pass


def _search_last_primary(raw: bytes) -> Maybe[Tuple[int, PrimaryByte]]:
    last = len(raw) - 1
    for i in range(len(raw)):
        p = new_primary_byte(raw[last - i]).value_or(None)
        if p is not None:
            return Maybe.from_value((last - i, p))
    return Maybe.empty()


def utf8_byte_truncate(text: str, max_bytes: int) -> ResultE[str]:
    if max_bytes < 0:
        return Result.failure(ValueError("max_bytes must be >= 0"))
    if max_bytes == 0:
        return Result.success("")
    utf8 = text.encode("utf8")
    if len(utf8) <= max_bytes:
        return Result.success(utf8.decode("utf8"))
    pre_truncated = utf8[:max_bytes]
    last_prim = _search_last_primary(pre_truncated)

    def _inner(last_prim_byte_index: int, last_prim_byte: PrimaryByte) -> str:
        bytes_after_last_prim = max_bytes - 1 - last_prim_byte_index
        if secondary_bytes_of(last_prim_byte) == bytes_after_last_prim:
            # char bytes fits in the truncation
            return pre_truncated.decode("utf8")
        # discard incomplete char
        return pre_truncated[:last_prim_byte_index].decode("utf8")

    return (
        last_prim.map(lambda p: _inner(p[0], p[1]))
        .to_result()
        .alt(lambda _: NotFound("No `PrimaryByte` was found!"))
    )
