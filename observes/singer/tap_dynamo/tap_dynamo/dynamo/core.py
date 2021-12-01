from __future__ import (
    annotations,
)

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
    FrozenList,
)
from typing import (
    Set,
    Type,
    Union,
)

Scalar = Union[str, int, Decimal, Binary, bool, Type[None]]
DynamoSet = Union[Set[str], Set[int], Set[Decimal], Set[Binary]]


@dataclass(frozen=True)
class DynamoValue:
    value: Union[
        Scalar,
        DynamoSet,
        FrozenList[DynamoValue],
        FrozenDict[str, DynamoValue],
    ]

    def unfold(
        self,
    ) -> Union[
        Scalar,
        DynamoSet,
        FrozenList[DynamoValue],
        FrozenDict[str, DynamoValue],
    ]:
        return self.value


DynamoItem = FrozenDict[str, DynamoValue]
