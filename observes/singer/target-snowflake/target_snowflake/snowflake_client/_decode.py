# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    Result,
    ResultE,
)
import re
from target_snowflake.snowflake_client.data_type import (
    DataType,
    PrecisionType,
    PrecisionTypes,
    ScaleType,
    ScaleTypes,
    StaticTypes,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def _value_error_handler(function: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(function())
    except ValueError as err:
        return Result.failure(err)


def _from_enum(transform: Callable[[_T], _R], raw: _T) -> ResultE[_R]:
    return _value_error_handler(lambda: transform(raw))


def _assert_str(raw: _T) -> ResultE[str]:
    if isinstance(raw, str):
        return Result.success(raw)
    err = TypeError(f"Expected `str` got `{type(raw)}`")
    return Result.failure(err)


def _str_to_int(raw: str) -> ResultE[int]:
    return _value_error_handler(lambda: int(raw))


def _decode_static(raw: str) -> ResultE[StaticTypes]:
    return _from_enum(StaticTypes, raw.upper())


def _decode_precision(raw: str) -> ResultE[PrecisionType]:
    pattern = r"^(\w+)\((\d+)\)$"
    match = re.match(pattern, raw)
    if match:
        raw_type = _assert_str(match.group(1))  # type: ignore[misc]
        _type = raw_type.bind(lambda r: _from_enum(PrecisionTypes, r.upper()))
        raw_precision = _assert_str(match.group(2))  # type: ignore[misc]
        _precision = raw_precision.bind(_str_to_int)
        return _type.bind(
            lambda t: _precision.map(lambda p: PrecisionType(t, p))
        )
    err = ValueError(f"_decode_precision regex does not match raw: {raw}")
    return Result.failure(err)


def _decode_scale(raw: str) -> ResultE[ScaleType]:
    pattern = r"^(\w+)\((\d+),(\d+)\)$"
    match = re.match(pattern, raw)
    if match:
        raw_type = _assert_str(match.group(1))  # type: ignore[misc]
        _type = raw_type.bind(lambda r: _from_enum(ScaleTypes, r.upper()))
        raw_precision = _assert_str(match.group(2))  # type: ignore[misc]
        _precision = raw_precision.bind(_str_to_int)
        raw_scale = _assert_str(match.group(3))  # type: ignore[misc]
        _scale = raw_scale.bind(_str_to_int)
        return _type.bind(
            lambda t: _precision.bind(
                lambda p: _scale.map(lambda s: ScaleType(t, p, s))
            )
        )
    err = ValueError(f"_decode_scale regex does not match raw: {raw}")
    return Result.failure(err)


def decode_type(raw: str) -> ResultE[DataType]:
    return (
        _decode_static(raw)
        .map(DataType)
        .lash(lambda _: _decode_precision(raw).map(DataType))
        .lash(lambda _: _decode_scale(raw).map(DataType))
    )
