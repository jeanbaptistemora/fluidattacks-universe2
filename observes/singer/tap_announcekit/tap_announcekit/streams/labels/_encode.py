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
from tap_announcekit.objs.label import (
    Label,
    LabelObj,
)
from typing import (
    Dict,
)

_encoder = ObjEncoder({})


def _schema() -> JsonSchema:
    props = Label.__annotations__.copy()
    props["label_id"] = str
    props["project_id"] = str
    return _encoder.to_jschema(props)


def _to_json(f_obj: LabelObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "label_id": f_obj.id_obj.id_str,
        "project_id": f_obj.id_obj.proj.id_str,
        "name": f_obj.obj.name,
        "color": f_obj.obj.color,
    }
    return JsonFactory.from_prim_dict(json)


@dataclass(frozen=True)
class LabelObjEncoders:
    stream_name: str

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"label_id", "project_id"})
        return SingerSchema(self.stream_name, _schema(), p_keys)

    def to_singer(self, obj: LabelObj) -> SingerRecord:
        return SingerRecord(self.stream_name, _to_json(obj))
