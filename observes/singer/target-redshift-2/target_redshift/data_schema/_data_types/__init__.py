# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .._utils import (
    opt_transform,
)
from ._integer import (
    int_handler,
)
from ._number import (
    num_handler,
)
from ._string import (
    string_format_handler,
)
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenList,
    JsonObj,
    Result,
    ResultE,
)
from fa_purity.union import (
    UnionFactory,
)
from redshift_client.column import (
    Column,
)
from redshift_client.data_type.core import (
    DataType,
    StaticTypes,
)
from target_redshift.errors import (
    MissingKey,
)
from typing import (
    Callable,
)


class _JschemaType(Enum):
    string = "string"
    number = "number"
    integer = "integer"
    object = "object"
    array = "array"
    boolean = "boolean"
    null = "null"


def _to_jschema_type(raw: str) -> ResultE[_JschemaType]:
    try:
        return Result.success(_JschemaType(raw.lower()))
    except ValueError as err:
        return Result.failure(err)


@dataclass(frozen=True)
class _RawType:
    raw_type: _JschemaType
    nullable: bool


def _simplify_type_list(types: FrozenList[str]) -> ResultE[_RawType]:
    _filter: Callable[[str], bool] = lambda x: x != "null"
    nullable = "null" in types
    reduced = tuple(filter(_filter, types))
    if len(reduced) > 1:
        err = NotImplementedError(
            "Generic union types not supported. Only Optional[_T] support"
        )
        return Result.failure(err)
    elif len(reduced) == 0:
        err = NotImplementedError(
            "None type field not supported. None type cannot hold information"
        )
        return Result.failure(err)
    return _to_jschema_type(reduced[0]).map(lambda t: _RawType(t, nullable))


def _to_list(item: str | FrozenList[str]) -> FrozenList[str]:
    return (item,) if isinstance(item, str) else item


def _to_column(raw: _RawType, encoded: JsonObj) -> ResultE[Column]:
    if raw.raw_type is _JschemaType.integer:
        return int_handler(encoded).map(
            lambda d: Column(d, raw.nullable, None)
        )
    if raw.raw_type is _JschemaType.number:
        return num_handler(encoded).map(
            lambda d: Column(d, raw.nullable, None)
        )
    if raw.raw_type is _JschemaType.string:
        return string_format_handler(encoded).map(
            lambda d: Column(d, raw.nullable, None)
        )
    if raw.raw_type is _JschemaType.boolean:
        return (
            Result.success(StaticTypes.BOOLEAN, Exception)
            .map(DataType)
            .map(lambda d: Column(d, raw.nullable, None))
        )
    err = NotImplementedError(f"Unsupported json schema type `{raw.raw_type}`")
    return Result.failure(err)


def jschema_type_handler(encoded: JsonObj) -> ResultE[Column]:
    _union: UnionFactory[str, FrozenList[str]] = UnionFactory()
    _types = (
        opt_transform(
            encoded,
            "type",
            lambda t: t.to_primitive(str)
            .map(_union.inl)
            .lash(lambda _: t.to_list_of(str).map(_union.inr)),
        )
        .to_result()
        .alt(lambda _: MissingKey("`type`", encoded))
        .alt(Exception)
        .bind(lambda b: b.alt(Exception))
    )
    return (
        _types.map(_to_list)
        .bind(_simplify_type_list)
        .bind(lambda r: _to_column(r, encoded))
    )
