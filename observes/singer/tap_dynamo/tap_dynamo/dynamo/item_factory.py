from boto3.dynamodb.types import (
    Binary,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from purity.v1 import (
    FrozenDict,
    InvalidType,
)
from tap_dynamo.dynamo.core import (
    DynamoSet,
    DynamoValue,
)
from typing import (
    Any,
    FrozenSet,
    Set,
    Type,
    TypeVar,
)

_T = TypeVar("_T")


def _from_set_any(raw: FrozenSet[Any], _type: Type[_T]) -> FrozenSet[_T]:
    temp: Set[_T] = set()
    for item in raw:
        if isinstance(item, _type):
            temp.add(item)
        else:
            raise InvalidType("_from_set_any", str(_type), item)
    return frozenset(temp)


def _assert_str(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    raise InvalidType("_assert_str", "str", raw)


@dataclass(frozen=True)
class ItemFactory:
    @classmethod
    def from_set(cls, raw: FrozenSet[Any]) -> DynamoSet:
        try:
            element = next(iter(raw))
        except StopIteration as err:
            raise InvalidType("from_set", "NonEmpty Set[Any]", raw) from err
        if isinstance(element, str):
            return _from_set_any(raw, str)
        if isinstance(element, int):
            return _from_set_any(raw, int)
        if isinstance(element, Decimal):
            return _from_set_any(raw, Decimal)
        if isinstance(element, Binary):
            return _from_set_any(raw, Binary)
        raise InvalidType("from_set", "SetScalar", raw)

    @classmethod
    def from_any(cls, raw: Any) -> DynamoValue:
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
        raise InvalidType("from_any", "unfold(DynamoValue)", raw)
