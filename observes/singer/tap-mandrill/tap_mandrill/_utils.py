# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil import (
    parser,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    unsafe_unwrap,
)
from logging import (
    Logger,
)
from typing import (
    Callable,
    NoReturn,
    TypeVar,
)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


@dataclass(frozen=True)
class ErrorAtInput(Exception):
    err: Exception
    input: str

    def __str__(self) -> str:
        return f"{self.err}"

    def raise_err(self, log: Logger) -> NoReturn:
        log.error("%s @ input = %s", self.err, self.input)
        raise self


def merge_maybe_result(item: Maybe[Result[_S, _F]]) -> Result[Maybe[_S], _F]:
    return item.map(lambda r: r.map(lambda v: Maybe.from_value(v))).value_or(
        Result.success(Maybe.empty())
    )


def handle_value_error(non_total_function: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(non_total_function())
    except ValueError as err:
        return Result.failure(err)


def isoparse(raw: str) -> ResultE[datetime]:
    return handle_value_error(lambda: parser.isoparse(raw))


def to_int(raw: str) -> ResultE[int]:
    return handle_value_error(lambda: int(raw))


def get_item(raw: FrozenDict[str, _T], key: str) -> ResultE[_T]:
    return (
        Maybe.from_optional(raw.get(key))
        .to_result()
        .alt(lambda _: KeyError(key))
    )
