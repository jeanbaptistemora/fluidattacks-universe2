from __future__ import (
    annotations,
)

from decimal import (
    Decimal,
)
from typing import (
    Any,
    TypeVar,
)
from typing_extensions import (
    TypeGuard,
)

Primitive = str | int | float | Decimal | bool | None
PrimitiveTypes = (
    type[str]
    | type[int]
    | type[float]
    | type[Decimal]
    | type[bool]
    | type[None]
)
PrimitiveTVar = TypeVar(
    "PrimitiveTVar", str, int, float, Decimal, bool, type[None]
)
NotNonePrimTvar = TypeVar("NotNonePrimTvar", str, int, float, Decimal, bool)


def is_primitive(raw: Any) -> TypeGuard[Primitive]:
    primitives = (str, int, float, bool, Decimal, type(None))
    if isinstance(raw, primitives):
        return True
    return False
