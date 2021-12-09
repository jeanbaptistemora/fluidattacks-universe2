from __future__ import (
    annotations,
)

from decimal import (
    Decimal,
)
from typing import (
    Type,
    TypeVar,
    Union,
)

Primitive = Union[str, int, float, Decimal, bool, None]
PrimitiveTypes = Union[
    Type[str],
    Type[int],
    Type[float],
    Type[Decimal],
    Type[bool],
    Type[None],
]
PrimitiveTVar = TypeVar(
    "PrimitiveTVar", str, int, float, Decimal, bool, Type[None]
)
NotNonePrimTvar = TypeVar("NotNonePrimTvar", str, int, float, Decimal, bool)
