from dataclasses import (
    dataclass,
)
from purity.v1 import (
    Transform,
)
from returns.curry import (
    partial,
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
from tap_announcekit.objs.id_objs import (
    ExtUserId,
)
from tap_announcekit.objs.post.feedback import (
    ActionSource,
    Feedback,
    FeedbackObj,
)
from tap_announcekit.stream import (
    SingerEncoder,
)
from typing import (
    Dict,
)

_str_type = JsonSchemaFactory.from_prim_type(str).to_json()
_encoder = ObjEncoder(
    {
        ActionSource: _str_type,
        ExtUserId: _str_type,
    }
)


def _schema() -> JsonSchema:
    props = Feedback.__annotations__.copy()
    props["feedback_id"] = str
    props["project_id"] = str
    props["post_id"] = str
    return _encoder.to_jschema(props)


def _to_json(f_obj: FeedbackObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "feedback_id": f_obj.id_obj.id_str,
        "project_id": f_obj.id_obj.post.proj.id_str,
        "post_id": f_obj.id_obj.post.id_str,
        "reaction": f_obj.obj.reaction,
        "comment": f_obj.obj.comment,
        "source": f_obj.obj.source.value,
        "created_at": f_obj.obj.created_at.isoformat(),
        "external_user_id": f_obj.obj.external_user_id.id_str,
    }
    return JsonFactory.from_prim_dict(json)


def _to_singer(stream_name: str, obj: FeedbackObj) -> SingerRecord:
    return SingerRecord(stream_name, _to_json(obj))


@dataclass(frozen=True)
class FeedbackObjEncoders:
    @staticmethod
    def encoder(stream_name: str) -> SingerEncoder[FeedbackObj]:
        p_keys = frozenset({"feedback_id", "project_id", "post_id"})
        schema = SingerSchema(stream_name, _schema(), p_keys)
        return SingerEncoder(
            schema, Transform(partial(_to_singer, stream_name))
        )
