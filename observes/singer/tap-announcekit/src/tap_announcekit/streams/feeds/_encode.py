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
from tap_announcekit.objs.feed import (
    Feed,
    FeedObj,
)
from typing import (
    Dict,
)

_encoder = ObjEncoder({})


def _schema() -> JsonSchema:
    props = Feed.__annotations__.copy()
    props["feed_id"] = str
    props["project_id"] = str
    return _encoder.to_jschema(props)


def _to_json(f_obj: FeedObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "feed_id": f_obj.id_obj.id_str,
        "project_id": f_obj.id_obj.proj.id_str,
        "name": f_obj.obj.name,
        "slug": f_obj.obj.slug,
        "created_at": f_obj.obj.created_at.isoformat(),
        "custom_host": f_obj.obj.custom_host,
        "website": f_obj.obj.website,
        "color": f_obj.obj.color,
        "url": f_obj.obj.url,
        "is_unindexed": f_obj.obj.is_unindexed,
        "is_private": f_obj.obj.is_private,
        "is_readmore": f_obj.obj.is_readmore,
        "html_inject": f_obj.obj.html_inject,
        "metadata": f_obj.obj.metadata,
        "theme": f_obj.obj.theme,
        "version": f_obj.obj.version,
    }
    return JsonFactory.from_prim_dict(json)


@dataclass(frozen=True)
class FeedObjEncoders:
    stream_name: str

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"feed_id", "project_id"})
        return SingerSchema(self.stream_name, _schema(), p_keys)

    def to_singer(self, obj: FeedObj) -> SingerRecord:
        return SingerRecord(self.stream_name, _to_json(obj))
