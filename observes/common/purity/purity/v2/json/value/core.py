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
from purity.v2.json.primitive.core import (
    Primitive,
)
from typing import (
    Union,
)

UnfoldedJVal = Union[
    FrozenDict[str, "JsonValue"], FrozenList["JsonValue"], Primitive
]


@dataclass(frozen=True)
class JsonValue:
    _value: UnfoldedJVal

    def unfold(
        self,
    ) -> UnfoldedJVal:
        return self._value
