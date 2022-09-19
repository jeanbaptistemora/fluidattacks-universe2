# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

# ref https://docs.snowflake.com/en/sql-reference/intro-summary-data-types.html

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from typing import (
    Callable,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


class StaticTypes(Enum):
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIME = "TIME"
    FLOAT = "FLOAT"


class PrecisionTypes(Enum):
    TIMESTAMP_LTZ = "TIMESTAMP_LTZ"  # with Local Time Zone
    TIMESTAMP_NTZ = "TIMESTAMP_NTZ"  # No Time Zone
    TIMESTAMP_TZ = "TIMESTAMP_TZ"  # with Time Zone (only the UTC offset)
    VARCHAR = "VARCHAR"
    BINARY = "BINARY"


class ScaleTypes(Enum):
    NUMBER = "DECIMAL"


@dataclass(frozen=True)
class NonStcDataTypes:
    _value: PrecisionTypes | ScaleTypes

    def map(
        self,
        transform_1: Callable[[PrecisionTypes], _T],
        transform_2: Callable[[ScaleTypes], _T],
    ) -> _T:
        if isinstance(self._value, PrecisionTypes):
            return transform_1(self._value)
        if isinstance(self._value, ScaleTypes):
            return transform_2(self._value)


@dataclass(frozen=True)
class PrecisionType:
    data_type: PrecisionTypes
    precision: int


@dataclass(frozen=True)
class ScaleType:
    data_type: ScaleTypes
    precision: int
    scale: int


@dataclass(frozen=True)
class DataType:
    _value: Union[StaticTypes, PrecisionType, ScaleType]

    def map(
        self,
        transform_1: Callable[[StaticTypes], _T],
        transform_2: Callable[[PrecisionType], _T],
        transform_3: Callable[[ScaleType], _T],
    ) -> _T:
        if isinstance(self._value, StaticTypes):
            return transform_1(self._value)
        if isinstance(self._value, PrecisionType):
            return transform_2(self._value)
        if isinstance(self._value, ScaleType):
            return transform_3(self._value)
