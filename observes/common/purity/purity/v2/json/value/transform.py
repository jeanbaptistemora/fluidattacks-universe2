from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v2.frozen import (
    FrozenDict,
    FrozenList,
)
from purity.v2.json.errors import (
    invalid_type,
)
from purity.v2.json.errors.invalid_type import (
    InvalidType,
)
from purity.v2.json.primitive.core import (
    Primitive,
    PrimitiveTVar,
)
from purity.v2.json.primitive.factory import (
    to_primitive,
)
from purity.v2.json.value.core import (
    JsonValue,
    UnfoldedJVal,
)
from returns.primitives.exceptions import (
    UnwrapFailedError,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
UnfoldResult = Result[_T, InvalidType]


@dataclass(frozen=True)
class Unfolder:
    jval: JsonValue

    @property
    def value(self) -> UnfoldedJVal:
        return self.jval.unfold()

    def to_list(self) -> UnfoldResult[FrozenList[JsonValue]]:
        if isinstance(self.value, tuple):
            return Success(self.value)
        return Failure(
            invalid_type.new("to_list", "FrozenList[JsonValue]", self.value)
        )

    def to_opt_list(self) -> UnfoldResult[Optional[FrozenList[JsonValue]]]:
        return Success(None) if self.value is None else self.to_list()

    def to_list_of(
        self, prim_type: Type[PrimitiveTVar]
    ) -> UnfoldResult[FrozenList[PrimitiveTVar]]:
        try:
            return self.to_list().map(
                lambda l: tuple(
                    to_primitive(i._value, prim_type).unwrap() for i in l
                )
            )
        except UnwrapFailedError:
            return Failure(
                invalid_type.new(
                    "to_list_of", f"FrozenList[{prim_type}]", prim_type
                )
            )

    def to_unfolder_list(self) -> UnfoldResult[FrozenList[Unfolder]]:
        return self.to_list().map(lambda l: tuple(Unfolder(i) for i in l))

    def to_json(self) -> UnfoldResult[FrozenDict[str, JsonValue]]:
        if isinstance(self.value, FrozenDict):
            return Success(self.value)
        return Failure(
            invalid_type.new(
                "to_json", "FrozenDict[str, JsonValue]", self.value
            )
        )

    def to_dict_of(
        self, prim_type: Type[PrimitiveTVar]
    ) -> UnfoldResult[FrozenDict[str, PrimitiveTVar]]:
        try:
            return self.to_json().map(
                lambda d: FrozenDict(
                    {
                        key: to_primitive(val, prim_type).unwrap()
                        for key, val in d.items()
                    }
                )
            )
        except UnwrapFailedError:
            return Failure(
                invalid_type.new(
                    f"to_dict_of", f"Dict[str, {prim_type}]", self.value
                )
            )


def to_raw(jval: JsonValue) -> Union[Dict[str, Any], List[Any], Primitive]:
    value = jval.unfold()
    if isinstance(value, tuple):
        return [to_raw(item) for item in value]
    if isinstance(value, FrozenDict):
        return {key: to_raw(val) for key, val in value.items()}
    return value
