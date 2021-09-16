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
    Optional,
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


PrimitiveType = TypeVar("PrimitiveType", str, int, float, bool)
PrimitiveTypes = Union[
    Type[str],
    Type[int],
    Type[float],
    Type[bool],
    Type[None],
]


def to_primitive(raw: Any, prim_type: Type[PrimitiveType]) -> PrimitiveType:
    if isinstance(raw, prim_type):
        return raw
    raise InvalidType(f"{type(raw)} expected a PrimitiveType")


def to_opt_primitive(
    raw: Any, prim_type: Type[PrimitiveType]
) -> Optional[PrimitiveType]:
    if isinstance(raw, prim_type):
        return raw
    if raw is None:
        return None
    raise InvalidType(f"{type(raw)} expected a PrimitiveType | None")


@dataclass(frozen=True)
class JsonValue:
    value: Union[Dict[str, JsonValue], List[JsonValue], Primitive]

    def unfold(
        self,
    ) -> Union[Dict[str, JsonValue], List[JsonValue], Primitive]:
        return self.value

    def to_raw(self) -> Union[Dict[str, Any], List[Any], Primitive]:
        raw = self.value
        if isinstance(raw, list):
            return [item.to_raw() for item in raw]
        if isinstance(raw, dict):
            return {key: val.to_raw() for key, val in raw.items()}
        return raw

    def to_primitive(self, prim_type: Type[PrimitiveType]) -> PrimitiveType:
        if isinstance(self.value, prim_type):
            return self.value
        raise InvalidType(f"{type(self.value)} expected a PrimitiveType")

    def to_list_of(
        self, prim_type: Type[PrimitiveType]
    ) -> List[PrimitiveType]:
        if isinstance(self.value, list):
            return [item.to_primitive(prim_type) for item in self.value]
        raise InvalidType(f"{type(self.value)} expected list")

    def to_list(self) -> List[JsonValue]:
        if isinstance(self.value, list):
            return self.value
        raise InvalidType(f"{type(self.value)} expected list")

    def to_opt_list(self) -> Optional[List[JsonValue]]:
        return None if self.value is None else self.to_list()

    def to_dict_of(
        self, prim_type: Type[PrimitiveType]
    ) -> Dict[str, PrimitiveType]:
        if isinstance(self.value, dict):
            return {
                key: val.to_primitive(prim_type)
                for key, val in self.value.items()
            }
        raise InvalidType(f"{type(self.value)} expected dict")

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

    @classmethod
    def from_json(cls, json_obj: JsonObj) -> Dict[str, Any]:
        return {key: val.to_raw() for key, val in json_obj.items()}


@dataclass(frozen=True)
class JsonValFactory:
    @classmethod
    def from_list(cls, raw: List[Primitive]) -> JsonValue:
        return JsonValue([JsonValue(item) for item in raw])

    @classmethod
    def from_dict(cls, raw: Dict[str, Primitive]) -> JsonValue:
        return JsonValue({key: JsonValue(val) for key, val in raw.items()})

    @classmethod
    def from_any(cls, raw: Any) -> JsonValue:
        if isinstance(raw, primitives) or raw is None:
            return JsonValue(raw)
        if isinstance(raw, dict):
            json_dict = {
                _is_str(key): cls.from_any(val) for key, val in raw.items()
            }
            return JsonValue(json_dict)
        if isinstance(raw, list):
            checked_list = [cls.from_any(item) for item in raw]
            return JsonValue(checked_list)
        raise InvalidType(f"{type(raw)} expected unfold(JsonValue)")


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


class CustomJsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, JsonValue):
            return o.unfold()
        return JSONEncoder.default(self, o)


@dataclass(frozen=True)
class JsonEmitter:
    # pylint: disable=no-self-use
    target: IO_FILE[str] = sys.stdout

    def to_str(self, json_obj: JsonObj, **kargs: Any) -> str:
        return json.dumps(json_obj, cls=CustomJsonEncoder, **kargs)

    def emit(self, json_obj: JsonObj) -> IO[None]:
        json.dump(json_obj, self.target, cls=CustomJsonEncoder)
        self.target.write("\n")
        return IO(None)
