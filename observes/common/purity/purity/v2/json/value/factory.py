from purity.v2.frozen import (
    FrozenDict,
    FrozenList,
)
from purity.v2.json.errors import (
    invalid_type,
)
from purity.v2.json.errors.invalid_type import (
    InvalidType,
)
from purity.v2.json.primitive import (
    factory as prim_factory,
)
from purity.v2.json.primitive.core import (
    is_primitive,
    Primitive,
)
from purity.v2.json.value.core import (
    JsonValue,
)
from returns.functions import (
    raise_exception,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)


def from_list(raw: Union[List[Primitive], FrozenList[Primitive]]) -> JsonValue:
    return JsonValue(tuple(JsonValue(item) for item in raw))


def from_dict(
    raw: Union[Dict[str, Primitive], FrozenDict[str, Primitive]]
) -> JsonValue:
    return JsonValue(
        FrozenDict({key: JsonValue(val) for key, val in raw.items()})
    )


def from_any(raw: Any) -> Result[JsonValue, InvalidType]:
    if is_primitive(raw):
        return Success(JsonValue(raw))
    if isinstance(raw, (FrozenDict, dict)):
        try:
            json_dict = FrozenDict(
                {
                    prim_factory.to_primitive(key, str)
                    .alt(raise_exception)
                    .unwrap(): from_any(val)
                    .alt(raise_exception)
                    .unwrap()
                    for key, val in raw.items()
                }
            )
            return Success(JsonValue(json_dict))
        except InvalidType as err:
            return Failure(err)
    if isinstance(raw, list):
        try:
            json_list = tuple(
                from_any(item).alt(raise_exception).unwrap() for item in raw
            )
            return Success(JsonValue(json_list))
        except InvalidType as err:
            return Failure(err)
    return Failure(invalid_type.new("from_any", "UnfoldedJVal", raw))
