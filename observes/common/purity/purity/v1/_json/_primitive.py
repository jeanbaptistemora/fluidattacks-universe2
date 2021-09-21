from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
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


class InvalidType(Exception):
    pass


Primitive = Union[str, int, float, bool, None]
PrimitiveTypes = Union[
    Type[str],
    Type[int],
    Type[float],
    Type[bool],
    Type[None],
]
PrimitiveTVar = TypeVar("PrimitiveTVar", str, int, float, bool, Type[None])


@dataclass(frozen=True)
class PrimitiveFactory:
    @staticmethod
    def is_primitive(raw: Any) -> TypeGuard[Primitive]:
        primitives = (str, int, float, bool, type(None))
        if isinstance(raw, primitives):
            return True
        return False

    @classmethod
    def to_primitive(
        cls, raw: Any, prim_type: Type[PrimitiveTVar]
    ) -> PrimitiveTVar:
        if isinstance(raw, prim_type):
            return raw
        raise InvalidType(f"{type(raw)} expected a PrimitiveType")

    @staticmethod
    def to_opt_primitive(
        raw: Any, prim_type: Type[PrimitiveTVar]
    ) -> PrimitiveTVar:
        if isinstance(raw, prim_type):
            return raw
        raise InvalidType(f"{type(raw)} expected a PrimitiveType | None")
