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
    PostContent,
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
    return _encoder.to_jschema(PostContent.__annotations__)


def _to_json(obj: PostContent) -> JsonObj:
    json: Dict[str, Primitive] = {
        "proj_id": obj.post_id.proj.proj_id,
        "post_id": obj.post_id.post_id,
        "locale_id": obj.locale_id,
        "title": obj.title,
        "body": obj.body,
        "slug": obj.slug,
        "url": obj.url,
    }
    return JsonFactory.from_prim_dict(json)


def _to_singer(stream_name: str, post: PostContent) -> SingerRecord:
    data = _to_json(post)
    return SingerRecord(stream_name, data)


@dataclass(frozen=True)
class PostEncoders:
    @staticmethod
    def encoder(stream_name: str) -> SingerEncoder[PostContent]:
        schema = SingerSchema(stream_name, _schema(), frozenset([]))
        return SingerEncoder(
            schema, Transform(partial(_to_singer, stream_name))
        )
