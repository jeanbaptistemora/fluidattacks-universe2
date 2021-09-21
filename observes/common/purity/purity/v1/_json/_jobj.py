from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from deprecated import (  # type: ignore
    deprecated,
)
import json
from purity.v1._json._jval import (
    JsonValFactory,
    JsonValue,
)
from purity.v1._json._primitive import (
    InvalidType,
    Primitive,
)
from typing import (
    Any,
    cast,
    Dict,
    IO as IO_FILE,
    List,
)

JsonObj = Dict[str, JsonValue]


class UnexpectedResult(Exception):
    pass


@dataclass(frozen=True)
class DictFactory:
    # assumptions
    @classmethod
    def loads(cls, raw_json: str) -> Dict[str, Any]:
        return cast(Dict[str, Any], json.loads(raw_json))

    @classmethod
    def load(cls, json_file: IO_FILE[str]) -> Dict[str, Any]:
        return cast(Dict[str, Any], json.load(json_file))

    @classmethod
    def from_json(cls, json_obj: JsonObj) -> Dict[str, Any]:
        return {key: val.to_raw() for key, val in json_obj.items()}


@dataclass(frozen=True)
class JsonFactory:
    @classmethod
    @deprecated(reason="migrated to JsonValFactory.from_any")
    def build_json_val(cls, raw: Any) -> JsonValue:
        return JsonValFactory.from_any(raw)

    @classmethod
    def build_json_list(cls, raw: Any) -> List[JsonObj]:
        if isinstance(raw, list):
            return [cls.from_any(item) for item in raw]
        raise InvalidType(f"{type(raw)} expected list")

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> JsonObj:
        result = JsonValFactory.from_any(raw).unfold()
        if isinstance(result, dict):
            return result
        raise UnexpectedResult("build_json not returned a JsonObj")

    @classmethod
    def from_prim_dict(cls, raw: Dict[str, Primitive]) -> JsonObj:
        return {key: JsonValue(val) for key, val in raw.items()}

    @classmethod
    def from_any(cls, raw: Any) -> JsonObj:
        if not isinstance(raw, dict):
            raise InvalidType("build_json expects a dict instance")
        return cls.from_dict(raw)

    @classmethod
    def loads(cls, raw_json: str) -> JsonObj:
        raw = DictFactory.loads(raw_json)
        return cls.from_dict(raw)

    @classmethod
    def load(cls, json_file: IO_FILE[str]) -> JsonObj:
        raw = DictFactory.load(json_file)
        return cls.from_dict(raw)
