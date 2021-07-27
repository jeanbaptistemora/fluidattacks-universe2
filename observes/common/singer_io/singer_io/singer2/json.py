from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import json
from json.encoder import (
    JSONEncoder,
)
from returns.io import (
    IO,
)
import sys
from typing import (
    Any,
    Dict,
    IO as IO_FILE,
    List,
    Type,
    TypeVar,
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


VarType = TypeVar("VarType", str, int, float, bool)


@dataclass(frozen=True)
class JsonValue:
    value: Union[Dict[str, JsonValue], List[JsonValue], Primitive]

    def unfold(
        self,
    ) -> Union[Dict[str, JsonValue], List[JsonValue], Primitive]:
        return self.value

    def to_primitive(self, prim_type: Type[VarType]) -> VarType:
        if isinstance(self.value, prim_type):
            return self.value
        raise InvalidType(f"{type(self.value)} expected str")

    def to_list_of(self, prim_type: Type[VarType]) -> List[VarType]:
        if isinstance(self.value, list):
            return [item.to_primitive(prim_type) for item in self.value]
        raise InvalidType(f"{type(self.value)} expected list")

    def to_json(self) -> Dict[str, JsonValue]:
        if isinstance(self.value, dict):
            return self.value
        raise InvalidType(f"{type(self.value)} expected dict")


JsonObj = Dict[str, JsonValue]


class UnexpectedResult(Exception):
    pass


@dataclass(frozen=True)
class DictFactory:
    # assumptions
    @classmethod
    def loads(cls, raw_json: str) -> Dict[str, Any]:
        return json.loads(raw_json)

    @classmethod
    def load(cls, json_file: IO_FILE[str]) -> Dict[str, Any]:
        return json.load(json_file)


@dataclass(frozen=True)
class JsonFactory:
    @classmethod
    def build_json_val(cls, raw: Any) -> JsonValue:
        if isinstance(raw, primitives) or raw is None:
            return JsonValue(raw)
        if isinstance(raw, dict):
            json_dict = {
                _is_str(key): cls.build_json_val(val)
                for key, val in raw.items()
            }
            return JsonValue(json_dict)
        if isinstance(raw, list):
            checked_list = [cls.build_json_val(item) for item in raw]
            return JsonValue(checked_list)
        raise InvalidType(f"{type(raw)} expected unfold(JsonValue)")

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> JsonObj:
        result = cls.build_json_val(raw).unfold()
        if isinstance(result, dict):
            return result
        raise UnexpectedResult("build_json not returned a JsonObj")

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


class CustomJsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, JsonValue):
            return o.unfold()
        return JSONEncoder.default(self, o)


@dataclass(frozen=True)
class JsonEmitter:
    target: IO_FILE[str] = sys.stdout

    def emit(self, json_obj: JsonObj) -> IO[None]:
        json.dump(json_obj, self.target, cls=CustomJsonEncoder)
        return IO(None)
