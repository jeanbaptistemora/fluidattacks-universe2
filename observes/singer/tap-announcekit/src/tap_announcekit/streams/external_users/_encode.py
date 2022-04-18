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
from tap_announcekit.objs.ext_user import (
    ExternalUser,
    ExtUserObj,
)
from typing import (
    Dict,
)

_encoder = ObjEncoder({})


def _schema() -> JsonSchema:
    props = ExternalUser.__annotations__.copy()
    props["ext_user_id"] = str
    props["project_id"] = str
    return _encoder.to_jschema(props)


def _to_json(f_obj: ExtUserObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "ext_user_id": f_obj.id_obj.id_str,
        "project_id": f_obj.id_obj.proj.id_str,
        "created_at": f_obj.obj.created_at.isoformat(),
        "seen_at": f_obj.obj.seen_at.isoformat(),
        "name": f_obj.obj.name,
        "email": f_obj.obj.email,
        "fields": f_obj.obj.fields,
        "is_anon": f_obj.obj.is_anon,
        "is_following": f_obj.obj.is_following,
        "is_email_verified": f_obj.obj.is_email_verified,
        "avatar": f_obj.obj.avatar,
        "is_app": f_obj.obj.is_app,
    }
    return JsonFactory.from_prim_dict(json)


@dataclass(frozen=True)
class ExtUserObjEncoders:
    stream_name: str

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"ext_user_id", "project_id"})
        return SingerSchema(self.stream_name, _schema(), p_keys)

    def to_singer(self, obj: ExtUserObj) -> SingerRecord:
        return SingerRecord(self.stream_name, _to_json(obj))
