# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.union import (
    UnionFactory,
)
from fa_purity.utils import (
    raise_exception,
)
from logging import (
    Logger,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


def raise_and_log(log: Logger, err: Exception, at_input: str) -> None:
    log.error("Error at input %s", at_input)
    raise_exception(err)


def int_to_str(num: int) -> str:
    return str(num)


def str_to_int(raw: str) -> ResultE[int]:
    try:
        return Result.success(int(raw))
    except ValueError as err:
        return Result.failure(err)


def str_to_datetime(raw: str) -> ResultE[datetime]:
    try:
        return Result.success(isoparse(raw))
    except ValueError as err:
        return Result.failure(err)


def merge_maybe_result(item: Maybe[Result[_S, _F]]) -> Result[Maybe[_S], _F]:
    _empty: Result[Maybe[_S], _F] = Result.success(Maybe.empty())
    return item.map(lambda r: r.map(lambda x: Maybe.from_value(x))).value_or(
        _empty
    )


@dataclass(frozen=True)
class JsonDecodeUtils:
    _data: JsonObj

    def get(self, key: str) -> Maybe[JsonValue]:
        return Maybe.from_optional(self._data.get(key))

    def require_generic(
        self, key: str, transform: Callable[[Unfolder], ResultE[_T]]
    ) -> ResultE[_T]:
        return (
            self.get(key)
            .to_result()
            .alt(lambda _: KeyError(key))
            .alt(Exception)
            .map(lambda j: Unfolder(j))
            .bind(transform)
            .alt(
                lambda e: Exception(
                    f"require_generic transform fail at key `{key}`. {e}"
                )
            )
        )

    def get_generic(
        self, key: str, transform: Callable[[Unfolder], ResultE[_T]]
    ) -> ResultE[Maybe[_T]]:
        _union: UnionFactory[_T, None] = UnionFactory()
        base = (
            self.get(key)
            .map(lambda j: Unfolder(j))
            .map(
                lambda u: u.to_none()
                .map(_union.inr)
                .alt(Exception)
                .lash(lambda _: transform(u).map(_union.inl))
                .map(lambda o: Maybe.from_optional(o))
            )
        )
        return (
            merge_maybe_result(base)
            .map(lambda m: m.bind(lambda x: x))
            .alt(
                lambda e: Exception(
                    f"get_generic transform fail at key {key}. {e}"
                )
            )
        )

    def get_str(self, key: str) -> ResultE[Maybe[str]]:
        return self.get_generic(
            key, lambda u: u.to_primitive(str).alt(Exception)
        )

    def get_float(self, key: str) -> ResultE[Maybe[float]]:
        return self.get_generic(
            key, lambda u: u.to_primitive(float).alt(Exception)
        )

    def get_datetime(self, key: str) -> ResultE[Maybe[datetime]]:
        return self.get_generic(
            key,
            lambda u: u.to_primitive(str).alt(Exception).bind(str_to_datetime),
        )

    def require_json(self, key: str) -> ResultE[JsonObj]:
        return self.require_generic(key, lambda u: u.to_json().alt(Exception))

    def require_list_of_str(self, key: str) -> ResultE[FrozenList[str]]:
        return self.require_generic(
            key, lambda u: u.to_list_of(str).alt(Exception)
        )

    def require_str(self, key: str) -> ResultE[str]:
        return self.require_generic(
            key, lambda u: u.to_primitive(str).alt(Exception)
        )

    def require_float(self, key: str) -> ResultE[float]:
        return self.require_generic(
            key, lambda u: u.to_primitive(float).alt(Exception)
        )

    def require_int(self, key: str) -> ResultE[int]:
        return self.require_generic(
            key, lambda u: u.to_primitive(int).alt(Exception)
        )

    def require_bool(self, key: str) -> ResultE[bool]:
        return self.require_generic(
            key, lambda u: u.to_primitive(bool).alt(Exception)
        )
