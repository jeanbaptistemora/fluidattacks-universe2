# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from target_snowflake.data_type import (
    DataType,
    PrecisionType,
    ScaleType,
    StaticTypes,
)


def _encode_static(data_type: StaticTypes) -> str:
    return data_type.value.upper()


def _encode_precision(data_type: PrecisionType) -> str:
    _type: str = data_type.data_type.value.upper()
    _precision: int = data_type.precision
    return f"{_type}({_precision})"


def _encode_scale(data_type: ScaleType) -> str:
    _type: str = data_type.data_type.value.upper()
    _precision: int = data_type.precision
    _scale: int = data_type.scale
    return f"{_type}({_precision},{_scale})"


def encode_type(data_type: DataType) -> str:
    return data_type.map(
        _encode_static,
        _encode_precision,
        _encode_scale,
    )
