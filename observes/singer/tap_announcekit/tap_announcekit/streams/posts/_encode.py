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
)
from tap_announcekit.objs.post import (
    Post,
)
from tap_announcekit.stream import (
    SingerEncoder,
)
from tap_announcekit.streams._obj_encoder import (
    StreamsObjsEncoder,
)
from typing import (
    Dict,
)

_encoder = StreamsObjsEncoder.encoder()


def _schema() -> JsonSchema:
    return _encoder.to_jschema(Post.__annotations__)


def _to_json(obj: Post) -> JsonObj:
    json: Dict[str, Primitive] = {
        "obj_id": obj.obj_id.id_str,
        "project_id": obj.obj_id.proj.id_str,
        "user_id": obj.user_id.id_str if obj.user_id else None,
        "created_at": obj.created_at.isoformat(),
        "visible_at": obj.visible_at.isoformat(),
        "image_id": obj.image_id.id_str if obj.image_id else None,
        "expire_at": obj.expire_at.isoformat() if obj.expire_at else None,
        "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        "is_draft": obj.is_draft,
        "is_pushed": obj.is_pushed,
        "is_pinned": obj.is_pinned,
        "is_internal": obj.is_internal,
        "external_url": obj.external_url,
        "segment_filters": obj.segment_filters,
    }
    return JsonFactory.from_prim_dict(json)


def _to_singer(stream_name: str, post: Post) -> SingerRecord:
    data = _to_json(post)
    return SingerRecord(stream_name, data)


@dataclass(frozen=True)
class PostEncoders:
    @staticmethod
    def encoder(stream_name: str) -> SingerEncoder[Post]:
        schema = SingerSchema(stream_name, _schema(), frozenset([]))
        return SingerEncoder(
            schema, Transform(partial(_to_singer, stream_name))
        )
