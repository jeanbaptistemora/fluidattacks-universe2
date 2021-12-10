from __future__ import (
    annotations,
)

from decimal import (
    Decimal,
)
from typing import (
    Any,
    Type,
    TypeVar,
    Union,
)
from typing_extensions import (
    TypeGuard,
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


def is_primitive(raw: Any) -> TypeGuard[Primitive]:
    primitives = (str, int, float, bool, Decimal, type(None))
    if isinstance(raw, primitives):
        return True
    return False
