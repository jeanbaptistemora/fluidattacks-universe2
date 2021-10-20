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
from tap_announcekit.objs.project import (
    Project,
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
    return _encoder.to_jschema(Project.__annotations__)


def _to_json(proj: Project) -> JsonObj:
    json: Dict[str, Primitive] = {
        "proj_id": proj.proj_id.proj_id,
        "encoded_id": proj.encoded_id,
        "name": proj.name,
        "slug": proj.slug,
        "website": proj.website,
        "is_authors_listed": proj.is_authors_listed,
        "is_whitelabel": proj.is_whitelabel,
        "is_subscribable": proj.is_subscribable,
        "is_slack_subscribable": proj.is_slack_subscribable,
        "is_feedback_enabled": proj.is_feedback_enabled,
        "is_demo": proj.is_demo,
        "is_readonly": proj.is_readonly,
        "image_id": proj.image_id.img_id if proj.image_id else None,
        "favicon_id": proj.favicon_id.img_id if proj.favicon_id else None,
        "created_at": proj.created_at.isoformat(),
        "ga_property": proj.ga_property,
        "avatar": proj.avatar,
        "locale": proj.locale,
        "uses_new_feed_hostname": proj.uses_new_feed_hostname,
        "payment_gateway": proj.payment_gateway,
        "trial_until": proj.trial_until.isoformat()
        if proj.trial_until
        else None,
        "metadata": proj.metadata,
    }
    return JsonFactory.from_prim_dict(json)


def _to_singer(stream_name: str, proj: Project) -> SingerRecord:
    data = _to_json(proj)
    return SingerRecord(stream_name, data)


@dataclass(frozen=True)
class ProjectEncoders:
    @staticmethod
    def encoder(stream_name: str) -> SingerEncoder[Project]:
        schema = SingerSchema(stream_name, _schema(), frozenset([]))
        return SingerEncoder(
            schema, Transform(partial(_to_singer, stream_name))
        )
