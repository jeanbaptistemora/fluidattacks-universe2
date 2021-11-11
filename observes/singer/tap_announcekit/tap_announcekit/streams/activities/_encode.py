from dataclasses import (
    dataclass,
)
from returns.maybe import (
    Maybe,
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
    JsonSchemaFactory,
)
from tap_announcekit.jschema import (
    ObjEncoder,
)
from tap_announcekit.objs.activity import (
    Activity,
    ActivityObj,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    FeedbackId,
    PostId,
)
from typing import (
    Dict,
)

_str_type = JsonSchemaFactory.from_prim_type(str).to_json()
_encoder = ObjEncoder(
    {
        ExtUserId: _str_type,
        PostId: _str_type,
        FeedbackId: _str_type,
    }
)


def _schema() -> JsonSchema:
    props = Activity.__annotations__.copy()
    props["activity_id"] = str
    props["project_id"] = str
    return _encoder.to_jschema(props)


def _to_json(f_obj: ActivityObj) -> JsonObj:
    ext_user = Maybe.from_optional(f_obj.obj.external_user_id).map(
        lambda i: i.id_str
    )
    post = Maybe.from_optional(f_obj.obj.external_user_id).map(
        lambda i: i.id_str
    )
    feedback = Maybe.from_optional(f_obj.obj.external_user_id).map(
        lambda i: i.id_str
    )
    json: Dict[str, Primitive] = {
        "activity_id": f_obj.id_obj.id_str,
        "project_id": f_obj.id_obj.proj.id_str,
        "type": f_obj.obj.type,
        "created_at": f_obj.obj.created_at.isoformat(),
        "external_user_id": ext_user.value_or(None),
        "post_id": post.value_or(None),
        "feedback_id": feedback.value_or(None),
    }
    return JsonFactory.from_prim_dict(json)


@dataclass(frozen=True)
class ActivityObjEncoder:
    stream_name: str

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"activity_id", "project_id"})
        return SingerSchema(self.stream_name, _schema(), p_keys)

    def to_singer(self, obj: ActivityObj) -> SingerRecord:
        return SingerRecord(self.stream_name, _to_json(obj))
