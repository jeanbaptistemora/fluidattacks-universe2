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
from tap_announcekit.jschema import (
    ObjEncoder,
)
from tap_announcekit.objs.post import (
    PostContent,
    PostContentObj,
)
from tap_announcekit.stream import (
    SingerEncoder,
)
from typing import (
    Dict,
)

_encoder = ObjEncoder({})


def _schema() -> JsonSchema:
    props = PostContent.__annotations__
    props["project_id"] = str
    props["post_id"] = str
    return _encoder.to_jschema(props)


def _to_json(p_obj: PostContentObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "project_id": p_obj.id_obj.proj.id_str,
        "post_id": p_obj.id_obj.id_str,
        "locale_id": p_obj.obj.locale_id,
        "title": p_obj.obj.title,
        "body": p_obj.obj.body,
        "slug": p_obj.obj.slug,
        "url": p_obj.obj.url,
    }
    return JsonFactory.from_prim_dict(json)


def _to_singer(stream_name: str, post: PostContentObj) -> SingerRecord:
    data = _to_json(post)
    return SingerRecord(stream_name, data)


@dataclass(frozen=True)
class PostContentEncoders:
    @staticmethod
    def encoder(stream_name: str) -> SingerEncoder[PostContentObj]:
        schema = SingerSchema(stream_name, _schema(), frozenset([]))
        return SingerEncoder(
            schema, Transform(partial(_to_singer, stream_name))
        )
