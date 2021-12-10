from __future__ import (
    annotations,
)

from purity.v2.frozen import (
    FrozenDict,
    FrozenList,
)
from purity.v2.json.errors import (
    invalid_type,
)
from purity.v2.json.primitive.core import (
    Primitive,
)
from purity.v2.json.value import (
    factory as jval_factory,
)
from purity.v2.json.value.core import (
    JsonValue,
)
from purity.v2.json.value.transform import (
    Unfolder,
    UnfoldResult,
)
from returns.functions import (
    raise_exception,
)
from returns.result import (
    Failure,
    Success,
)
import simplejson
from typing import (
    Any,
    cast,
    Dict,
    IO as IO_FILE,
)

JsonObj = FrozenDict[str, JsonValue]


class UnexpectedResult(Exception):
    pass


def from_any(raw: Any) -> UnfoldResult[JsonObj]:
    return jval_factory.from_any(raw).bind(lambda j: Unfolder(j).to_json())


def from_prim_dict(raw: Dict[str, Primitive]) -> JsonObj:
    return FrozenDict({key: JsonValue(val) for key, val in raw.items()})


def loads(raw: str) -> UnfoldResult[JsonObj]:
    raw_json = cast(Dict[str, Any], simplejson.loads(raw))
    return from_any(raw_json)


def load(raw: IO_FILE[str]) -> UnfoldResult[JsonObj]:
    raw_json = cast(Dict[str, Any], simplejson.load(raw))
    return from_any(raw_json)


def json_list(raw: Any) -> UnfoldResult[FrozenList[JsonObj]]:
    try:
        if isinstance(raw, (list, tuple)):
            return Success(
                tuple(
                    from_any(item).alt(raise_exception).unwrap()
                    for item in raw
                )
            )
        return Failure(invalid_type.new("json_list", "List|Tuple", raw))
    except invalid_type.InvalidType as err:
        return Failure(err)
