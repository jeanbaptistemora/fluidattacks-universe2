from fa_purity.frozen import (
    FrozenDict,
)
from fa_purity.json.value.core import (
    JsonValue,
)
from purity.v1._json._jval import (
    JsonValue as JsonValueV1,
)


def to_jval_v1(val: JsonValue) -> JsonValueV1:
    unfolded = val.unfold()
    if isinstance(unfolded, FrozenDict):
        return JsonValueV1({k: to_jval_v1(v) for k, v in unfolded.items()})
    if isinstance(unfolded, tuple):
        return JsonValueV1([to_jval_v1(v) for v in unfolded])
    return JsonValueV1(unfolded)
