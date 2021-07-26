from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import json
from typing import (
    Any,
    Dict,
    IO as IO_FILE,
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

    def unfold(
        self,
    ) -> Union[Dict[str, JsonValue], List[JsonValue], Primitive]:
        return self.value


JsonObj = Dict[str, JsonValue]


class UnexpectedResult(Exception):
    pass


@dataclass(frozen=True)
class JsonFactory:
    def build_json_val(self, raw: Any) -> JsonValue:
        if isinstance(raw, primitives) or raw is None:
            return JsonValue(raw)
        if isinstance(raw, dict):
            json_dict = {
                _is_str(key): self.build_json_val(val)
                for key, val in raw.items()
            }
            return JsonValue(json_dict)
        if isinstance(raw, list):
            checked_list = [self.build_json_val(item) for item in raw]
            return JsonValue(checked_list)
        raise InvalidType(f"{type(raw)} expected unfold(JsonValue)")

    def json_from_dict(self, raw: Dict[str, Any]) -> JsonObj:
        result = self.build_json_val(raw).unfold()
        if isinstance(result, dict):
            return result
        raise UnexpectedResult("build_json not returned a JsonObj")

    def build_json(self, raw: Any) -> JsonObj:
        if not isinstance(raw, dict):
            raise InvalidType("build_json expects a dict instance")
        return self.json_from_dict(raw)

    def loads(self, raw_json: str) -> JsonObj:
        raw = json.loads(raw_json)
        return self.build_json(raw)

    def load(self, json_file: IO_FILE[str]) -> JsonObj:
        raw = json.load(json_file)
        return self.build_json(raw)
