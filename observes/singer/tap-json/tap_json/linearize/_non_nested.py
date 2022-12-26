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
