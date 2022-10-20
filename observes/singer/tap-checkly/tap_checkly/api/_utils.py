# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse as _isoparse,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
    Stream,
)
from fa_purity.json.primitive.core import (
    NotNonePrimTvar,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_none,
)
from typing import (
    Callable,
    Type,
    TypeVar,
)


def isoparse(raw: str) -> ResultE[datetime]:
    try:
        return Result.success(_isoparse(raw))
    except ValueError as err:
        return Result.failure(err)


_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


def paginate_all(
    list_items: Callable[[int], Cmd[FrozenList[_T]]]
) -> Stream[_T]:
    return (
        infinite_range(1, 1)
        .map(list_items)
        .transform(lambda x: from_piter(x))
        .map(lambda i: i if bool(i) else None)
        .transform(lambda x: until_none(x))
        .map(lambda x: from_flist(x))
        .transform(lambda x: chain(x))
    )


def switch_maybe(item: Maybe[Result[_S, _F]]) -> Result[Maybe[_S], _F]:
    _empty: Result[Maybe[_S], _F] = Result.success(Maybe.empty())
    return item.map(lambda r: r.map(lambda x: Maybe.from_value(x))).value_or(
        _empty
    )


@dataclass(frozen=True)
class ExtendedUnfolder:
    json: JsonObj

    def unfolder(self) -> Unfolder:
        return Unfolder(JsonValue(self.json))

    def get(self, key: str) -> Maybe[JsonValue]:
        return Maybe.from_optional(self.json.get(key))

    def get_required(self, key: str) -> ResultE[JsonValue]:
        return (
            self.get(key)
            .to_result()
            .alt(lambda _: KeyError(key))
            .alt(Exception)
        )

    def require_primitive(
        self, key: str, prim_type: Type[NotNonePrimTvar]
    ) -> ResultE[NotNonePrimTvar]:
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(
                lambda u: u.to_primitive(prim_type)
                .alt(lambda e: TypeError(f"At `{key}` i.e. {e}"))
                .alt(Exception)
            )
        )

    def require_float(self, key: str) -> ResultE[float]:
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(
                lambda u: u.to_primitive(float)
                .alt(Exception)
                .lash(
                    lambda _: u.to_primitive(int)
                    .map(float)
                    .alt(lambda e: TypeError(f"At `{key}` i.e. {e}"))
                )
            )
        )

    def require_datetime(self, key: str) -> ResultE[datetime]:
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(lambda u: u.to_primitive(str).alt(Exception).bind(isoparse))
        )

    def opt_datetime(self, key: str) -> ResultE[Maybe[datetime]]:
        return switch_maybe(
            self.get(key)
            .map(Unfolder)
            .map(lambda u: u.to_primitive(str).alt(Exception).bind(isoparse))
        )
