from boto3.dynamodb.types import (
    Binary,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from fa_purity.frozen import (
    FrozenDict,
)
from fa_purity.json.errors.invalid_type import (
    new as invalid_type,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from fa_purity.utils import (
    raise_exception,
)
from tap_dynamo.dynamo.core import (
    DynamoSet,
    DynamoValue,
)
from typing import (
    cast,
    FrozenSet,
    Type,
    TypeVar,
)

_A = TypeVar("_A")
_T = TypeVar("_T")


def _from_set_any(raw: FrozenSet[_A], _type: Type[_T]) -> FrozenSet[_T]:
    for item in raw:
        if not isinstance(item, _type):
            raise invalid_type("_from_set_any", str(_type), item)
    return cast(FrozenSet[_T], raw)


def _assert_str(raw: _A) -> str:
    return to_primitive(raw, str).alt(raise_exception).unwrap()


@dataclass(frozen=True)
class ItemFactory:
    @classmethod
    def from_set(cls, raw: FrozenSet[_A]) -> DynamoSet:
        try:
            element = next(iter(raw))
        except StopIteration as err:
            raise invalid_type("from_set", "NonEmpty Set[_A]", raw) from err
        if isinstance(element, str):
            return _from_set_any(raw, str)
        if isinstance(element, int):
            return _from_set_any(raw, int)
        if isinstance(element, Decimal):
            return _from_set_any(raw, Decimal)
        if isinstance(element, Binary):
            return _from_set_any(raw, Binary)
        raise invalid_type("from_set", "SetScalar", raw)

    @classmethod
    def from_any(cls, raw: _A) -> DynamoValue:
        if raw is None or isinstance(raw, (str, int, Decimal, Binary, bool)):
            return DynamoValue(raw)
        if isinstance(raw, set):
            return DynamoValue(cls.from_set(frozenset(raw)))
        if isinstance(raw, frozenset):
            return DynamoValue(cls.from_set(raw))
        if isinstance(raw, (list, tuple)):
            return DynamoValue(tuple(cls.from_any(r) for r in raw))
        if isinstance(raw, dict):
            return DynamoValue(
                FrozenDict(
                    {_assert_str(k): cls.from_any(v) for k, v in raw.items()}
                )
            )
        raise invalid_type("from_any", "unfold(DynamoValue)", raw)
