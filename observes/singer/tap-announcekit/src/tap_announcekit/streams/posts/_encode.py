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
    ImageId,
    UserId,
)
from tap_announcekit.objs.post import (
    Post,
    PostObj,
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
        UserId: _str_type,
        ImageId: _str_type,
    }
)


def _schema() -> JsonSchema:
    props = Post.__annotations__.copy()
    props["post_id"] = str
    props["project_id"] = str
    return _encoder.to_jschema(props)


def _to_json(p_obj: PostObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "post_id": p_obj.id_obj.id_str,
        "project_id": p_obj.id_obj.proj.id_str,
        "user_id": p_obj.obj.user_id.id_str if p_obj.obj.user_id else None,
        "created_at": p_obj.obj.created_at.isoformat(),
        "visible_at": p_obj.obj.visible_at.isoformat(),
        "image_id": p_obj.obj.image_id.id_str if p_obj.obj.image_id else None,
        "expire_at": p_obj.obj.expire_at.isoformat()
        if p_obj.obj.expire_at
        else None,
        "updated_at": p_obj.obj.updated_at.isoformat()
        if p_obj.obj.updated_at
        else None,
        "is_draft": p_obj.obj.is_draft,
        "is_pushed": p_obj.obj.is_pushed,
        "is_pinned": p_obj.obj.is_pinned,
        "is_internal": p_obj.obj.is_internal,
        "external_url": p_obj.obj.external_url,
        "segment_filters": p_obj.obj.segment_filters,
    }
    return JsonFactory.from_prim_dict(json)


def _to_singer(stream_name: str, post: PostObj) -> SingerRecord:
    data = _to_json(post)
    return SingerRecord(stream_name, data)


@dataclass(frozen=True)
class PostEncoders:
    @staticmethod
    def encoder(stream_name: str) -> SingerEncoder[PostObj]:
        p_keys = frozenset({"post_id", "project_id"})
        schema = SingerSchema(stream_name, _schema(), p_keys)
        return SingerEncoder(
            schema, Transform(partial(_to_singer, stream_name))
        )
