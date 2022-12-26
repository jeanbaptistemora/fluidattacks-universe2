from ._non_nested import (
    JsonValueFlatDicts,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
)
from fa_purity.json.primitive import (
    Primitive,
)
import hashlib
from tap_json.clean_str import (
    CleanString,
)
from typing import (
    Callable,
)


def _data_hash(data: Primitive) -> str:
    hash_id = hashlib.sha256()
    hash_id.update(bytes(str(data), "utf-8"))
    return hash_id.hexdigest()


def _list_hash(
    data: FrozenList[JsonValueFlatDicts],
    hash_fx: Callable[[JsonValueFlatDicts], str],
) -> str:
    hash_id = hashlib.sha256()
    for item in data:
        hash_id.update(bytes(hash_fx(item), "utf-8"))
    return hash_id.hexdigest()


def _dict_hash(
    data: FrozenDict[CleanString, Primitive | FrozenList[JsonValueFlatDicts]],
    hash_fx: Callable[[JsonValueFlatDicts], str],
) -> str:
    hash_id = hashlib.sha256()
    for key, val in sorted(data.items()):
        hash_id.update(bytes(_data_hash(key.raw), "utf-8"))
        hash_val = (
            _list_hash(val, hash_fx)
            if isinstance(val, tuple)
            else _data_hash(val)
        )
        hash_id.update(bytes(hash_val, "utf-8"))
    return hash_id.hexdigest()


def struct_hash(value: JsonValueFlatDicts) -> str:
    return value.map(
        lambda x: _data_hash(x),
        lambda x: _list_hash(x, struct_hash),
        lambda x: _dict_hash(x, struct_hash),
    )
