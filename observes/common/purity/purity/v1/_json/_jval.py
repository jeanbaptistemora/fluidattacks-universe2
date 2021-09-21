from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v1._json._primitive import (
    InvalidType,
    Primitive,
    PrimitiveFactory,
    PrimitiveTVar,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
)


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

    def to_primitive(self, prim_type: Type[PrimitiveTVar]) -> PrimitiveTVar:
        if isinstance(self.value, prim_type):
            return self.value
        raise InvalidType(f"{type(self.value)} expected a PrimitiveType")

    def to_list_of(
        self, prim_type: Type[PrimitiveTVar]
    ) -> List[PrimitiveTVar]:
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
        self, prim_type: Type[PrimitiveTVar]
    ) -> Dict[str, PrimitiveTVar]:
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
        if PrimitiveFactory.is_primitive(raw):
            return JsonValue(raw)
        if isinstance(raw, dict):
            json_dict = {
                PrimitiveFactory.to_primitive(key, str): cls.from_any(val)
                for key, val in raw.items()
            }
            return JsonValue(json_dict)
        if isinstance(raw, list):
            checked_list = [cls.from_any(item) for item in raw]
            return JsonValue(checked_list)
        raise InvalidType(f"{type(raw)} expected unfold(JsonValue)")
