from ._core import (
    JsonValueFlatDicts,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.primitive import (
    Primitive,
)
from tap_json.clean_str import (
    CleanString,
)
from typing import (
    Callable,
    Dict,
    TypeVar,
)

FIELD_SEP: str = "__"

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


def _prefix_key(
    prefix: str, items: FrozenDict[str, _T]
) -> FrozenDict[str, _T]:
    return FrozenDict({prefix + k: v for k, v in items.items()})


def _merge_dicts(items: FrozenList[FrozenDict[_K, _V]]) -> FrozenDict[_K, _V]:
    result: Dict[_K, _V] = {}
    for i in items:
        result = result | i
    return freeze(result)


def _extract_dict(
    key: str,
    value: JsonValue,
    transform: Callable[[JsonValue], JsonValueFlatDicts],
) -> FrozenDict[CleanString, FrozenList[JsonValueFlatDicts] | Primitive]:
    return value.map(
        lambda x: FrozenDict({CleanString.new(key): x}),
        lambda items: FrozenDict(
            {CleanString.new(key): tuple(transform(i) for i in items)}
        ),
        lambda x: _merge_dicts(
            tuple(
                _extract_dict(k, v, transform)
                for k, v in _prefix_key(key + FIELD_SEP, x).items()
            )
        ),
    )


def flatten_nested_dict(value: JsonValue) -> JsonValueFlatDicts:
    return value.map(
        lambda x: JsonValueFlatDicts(x),
        lambda items: JsonValueFlatDicts(
            tuple(flatten_nested_dict(i) for i in items)
        ),
        lambda x: JsonValueFlatDicts(
            _merge_dicts(
                tuple(
                    _extract_dict(k, v, flatten_nested_dict)
                    for k, v in x.items()
                )
            )
        ),
    )


def simplify_json(
    data: JsonObj,
) -> FrozenDict[CleanString, FrozenList[JsonValueFlatDicts] | Primitive]:
    return _merge_dicts(
        tuple(
            _extract_dict(k, v, flatten_nested_dict) for k, v in data.items()
        )
    )
