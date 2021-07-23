from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)

primitives = (str, int, float, bool)
Primitive = Union[str, int, float, bool, None]


class InvalidType(Exception):
    pass


def _is_str(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    raise InvalidType(f"{type(obj)} expected str")


@dataclass(frozen=True)
class JsonValue:
    value: Union[Dict[str, JsonValue], List[JsonValue], Primitive]

    @classmethod
    def from_raw(cls, raw: Any) -> JsonValue:
        if isinstance(raw, primitives) or raw is None:
            return JsonValue(raw)
        if isinstance(raw, dict):
            json = {
                _is_str(key): cls.from_raw(val) for key, val in raw.items()
            }
            return JsonValue(json)
        if isinstance(raw, list):
            checked_list = [cls.from_raw(item) for item in raw]
            return JsonValue(checked_list)
        raise InvalidType(f"{type(raw)} expected unfold(JsonValue)")

    def unfold(
        self,
    ) -> Union[Dict[str, JsonValue], List[JsonValue], Primitive]:
        return self.value


JsonObj = Dict[str, JsonValue]
