from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
)
from fa_purity.json.primitive import (
    Primitive,
)
from tap_json.clean_str import (
    CleanString,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")
UnfoldedJsonValueFlatDicts = (
    FrozenList["JsonValueFlatDicts"]
    | FrozenDict[CleanString, FrozenList["JsonValueFlatDicts"] | Primitive]
    | Primitive
)


@dataclass(frozen=True)
class JsonValueFlatDicts:
    _value: UnfoldedJsonValueFlatDicts

    def unfold(
        self,
    ) -> UnfoldedJsonValueFlatDicts:
        return self._value

    def map(
        self,
        primitive_case: Callable[[Primitive], _T],
        list_case: Callable[[FrozenList[JsonValueFlatDicts]], _T],
        dict_case: Callable[
            [
                FrozenDict[
                    CleanString, FrozenList["JsonValueFlatDicts"] | Primitive
                ]
            ],
            _T,
        ],
    ) -> _T:
        if isinstance(self._value, tuple):
            return list_case(self._value)
        if isinstance(self._value, FrozenDict):
            return dict_case(self._value)
        return primitive_case(self._value)
