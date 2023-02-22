from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from purity.v2.json.primitive import (
    factory,
)
from purity.v2.json.primitive.core import (
    NotNonePrimTvar,
    Primitive,
    PrimitiveTVar,
    PrimitiveTypes,
)
from returns.functions import (
    raise_exception,
)
from typing import (
    Any,
    Optional,
    Type,
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
        return (
            factory.to_primitive(raw, prim_type).lash(raise_exception).unwrap()
        )

    @staticmethod
    def to_opt_primitive(
        raw: Any, prim_type: Type[NotNonePrimTvar]
    ) -> Optional[NotNonePrimTvar]:
        return (
            factory.to_opt_primitive(raw, prim_type)
            .lash(raise_exception)
            .unwrap()
        )


__all__ = [
    "Primitive",
    "PrimitiveTypes",
    "PrimitiveTVar",
    "NotNonePrimTvar",
]
