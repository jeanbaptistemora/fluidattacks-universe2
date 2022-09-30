# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .._utils import (
    opt_transform,
)
from fa_purity import (
    JsonObj,
    Result,
    ResultE,
)
from target_snowflake.snowflake_client.data_type import (
    DataType,
    PrecisionType,
    PrecisionTypes,
    StaticTypes,
)


def _format_handler(format: str, encoded: JsonObj) -> ResultE[DataType]:
    timezone: ResultE[bool] = opt_transform(
        encoded,
        "timezone",
        lambda u: u.to_primitive(bool).alt(
            lambda e: Exception(f"Error at timezone. {e}")
        ),
    ).value_or(Result.success(False))
    if format == "date-time":
        return timezone.map(
            lambda t: PrecisionType(PrecisionTypes.TIMESTAMP_TZ, 9)
            if t
            else PrecisionType(PrecisionTypes.TIMESTAMP_NTZ, 9)
        ).map(DataType)
    elif format == "time":
        return timezone.map(
            lambda t: PrecisionType(PrecisionTypes.TIME, 9),
        ).map(DataType)
    elif format == "date":
        return Result.success(StaticTypes.DATE, Exception).map(
            lambda x: DataType(x)
        )
    err = NotImplementedError(f"Not supported format '{format}'")
    return Result.failure(err)


def _string_handler(encoded: JsonObj) -> ResultE[DataType]:
    precision: ResultE[int] = opt_transform(
        encoded,
        "precision",
        lambda u: u.to_primitive(int).alt(
            lambda e: Exception(f"Error at precision. {e}")
        ),
    ).value_or(Result.success(256))

    return precision.map(
        lambda p: PrecisionType(PrecisionTypes.VARCHAR, p)
    ).map(DataType)


def string_format_handler(encoded: JsonObj) -> ResultE[DataType]:
    _format = opt_transform(
        encoded,
        "format",
        lambda u: u.to_primitive(str).alt(
            lambda e: Exception(f"Error at format. {e}")
        ),
    )
    return _format.map(
        lambda r: r.bind(lambda f: _format_handler(f, encoded))
    ).or_else_call(lambda: _string_handler(encoded))
