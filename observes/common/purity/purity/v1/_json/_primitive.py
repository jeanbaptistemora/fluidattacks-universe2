from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
    Union,
)
from typing_extensions import (
    TypeGuard,
)


class InvalidType(Exception):
    def __init__(
        self,
        caller: str,
        expected: str,
        item: Any,
    ):
        super().__init__(
            f"{caller} expected `{expected}` not `{str(type(item))}`"
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


@dataclass(frozen=True)
class PrimitiveFactory:
    @staticmethod
    def is_primitive(raw: Any) -> TypeGuard[Primitive]:
        primitives = (str, int, float, bool, Decimal, type(None))
        if isinstance(raw, primitives):
            return True
        return False

    @classmethod
    def to_primitive(
        cls, raw: Any, prim_type: Type[PrimitiveTVar]
    ) -> PrimitiveTVar:
        if isinstance(raw, prim_type):
            return raw
        raise InvalidType("to_primitive", str(prim_type), raw)

    @staticmethod
    def to_opt_primitive(
        raw: Any, prim_type: Type[NotNonePrimTvar]
    ) -> Optional[NotNonePrimTvar]:
        if raw is None or isinstance(raw, prim_type):
            return raw
        raise InvalidType("to_opt_primitive", f"{prim_type} | None", raw)
