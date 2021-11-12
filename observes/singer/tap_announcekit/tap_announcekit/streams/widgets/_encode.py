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
from tap_announcekit.objs.widget import (
    Widget,
    WidgetObj,
)
from typing import (
    Dict,
)

_encoder = ObjEncoder({})


def _schema() -> JsonSchema:
    props = Widget.__annotations__.copy()
    props["widget_id"] = str
    props["project_id"] = str
    return _encoder.to_jschema(props)


def _to_json(f_obj: WidgetObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "widget_id": f_obj.id_obj.id_str,
        "project_id": f_obj.id_obj.proj.id_str,
        "created_at": f_obj.obj.created_at.isoformat(),
        "name": f_obj.obj.name,
        "mode": f_obj.obj.mode,
        "action": f_obj.obj.action,
        "slug": f_obj.obj.slug,
        "options": f_obj.obj.options,
        "theme": f_obj.obj.theme,
        "version": f_obj.obj.version,
    }
    return JsonFactory.from_prim_dict(json)


@dataclass(frozen=True)
class WidgetObjEncoders:
    stream_name: str

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"widget_id", "project_id"})
        return SingerSchema(self.stream_name, _schema(), p_keys)

    def to_singer(self, obj: WidgetObj) -> SingerRecord:
        return SingerRecord(self.stream_name, _to_json(obj))
