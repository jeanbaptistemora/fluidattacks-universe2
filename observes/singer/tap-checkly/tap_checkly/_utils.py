# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import (
    annotations,
)

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
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.primitive.core import (
    NotNonePrimTvar,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.union import (
    UnionFactory,
)
from typing import (
    Optional,
    Type,
    TypeVar,
)

_S = TypeVar("_S")
_F = TypeVar("_F")


def isoparse(raw: str) -> ResultE[datetime]:
    try:
        return Result.success(_isoparse(raw), Exception)
    except ValueError as err:
        return Result.failure(err, datetime).alt(Exception)


def switch_maybe(item: Maybe[Result[_S, _F]]) -> Result[Maybe[_S], _F]:
    _empty: Maybe[_S] = Maybe.empty()
    _empty_result: Result[Maybe[_S], _F] = Result.success(_empty)
    return item.map(lambda r: r.map(lambda x: Maybe.from_value(x))).value_or(
        _empty_result
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

    def maybe_primitive(
        self, key: str, prim_type: Type[NotNonePrimTvar]
    ) -> ResultE[Maybe[NotNonePrimTvar]]:
        return switch_maybe(
            self.get(key)
            .map(Unfolder)
            .map(
                lambda u: u.to_optional(lambda uu: uu.to_primitive(prim_type))
                .map(lambda m: Maybe.from_optional(m))
                .alt(lambda e: TypeError(f"At `{key}` i.e. {e}"))
                .alt(Exception)
            )
        ).map(lambda m: m.bind(lambda x: x))

    def require_json(self, key: str) -> ResultE[JsonObj]:
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(lambda u: u.to_json().alt(Exception))
        )

    def require_opt_json(self, key: str) -> ResultE[Optional[JsonObj]]:
        factory: UnionFactory[JsonObj, None] = UnionFactory()
        return (
            self.get_required(key)
            .map(Unfolder)
            .bind(
                lambda u: u.to_json()
                .map(factory.inl)
                .lash(lambda _: u.to_none().map(factory.inr))
                .alt(Exception)
            )
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


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class DateInterval:
    _private: _Private
    oldest: datetime
    newest: datetime

    @staticmethod
    def new(oldest: datetime, newest: datetime) -> ResultE[DateInterval]:
        if newest > oldest:
            return Result.success(
                DateInterval(_Private(), oldest, newest), Exception
            )
        err = ValueError(
            f"Invalid DateInterval: oldest > newest. i.e. {oldest} > {newest}"
        )
        return Result.failure(err, DateInterval).alt(Exception)
