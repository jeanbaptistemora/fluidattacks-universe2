from dataclasses import (
    dataclass,
)
from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)
from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
    Primitive,
)
from singer_io.singer2.json_schema import (
    JsonSchema,
)
from tap_announcekit.jschema import (
    ObjEncoder,
)
from tap_announcekit.objs.segment import (
    SegmentField,
    SegmentProfile,
)
from typing import (
    Dict,
)

_encoder = ObjEncoder({})


@dataclass(frozen=True)
class SegmentFieldEncoder:
    stream_name: str

    @staticmethod
    def _schema() -> JsonSchema:
        props = SegmentField.__annotations__.copy()
        return _encoder.to_jschema(props)

    @staticmethod
    def _to_json(obj: SegmentField) -> JsonObj:
        json: Dict[str, Primitive] = {
            "proj": obj.proj.id_str,
            "field": obj.field,
        }
        return JsonFactory.from_prim_dict(json)

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"proj", "field"})
        return SingerSchema(self.stream_name, self._schema(), p_keys)

    def to_singer(self, obj: SegmentField) -> SingerRecord:
        return SingerRecord(self.stream_name, self._to_json(obj))


@dataclass(frozen=True)
class SegmentProfileEncoder:
    stream_name: str

    @staticmethod
    def _schema() -> JsonSchema:
        props = SegmentProfile.__annotations__.copy()
        return _encoder.to_jschema(props)

    @staticmethod
    def _to_json(obj: SegmentProfile) -> JsonObj:
        json: Dict[str, Primitive] = {
            "proj": obj.proj.id_str,
            "title": obj.title,
            "rules": obj.rules,
        }
        return JsonFactory.from_prim_dict(json)

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"proj", "title"})
        return SingerSchema(self.stream_name, self._schema(), p_keys)

    def to_singer(self, obj: SegmentProfile) -> SingerRecord:
        return SingerRecord(self.stream_name, self._to_json(obj))
