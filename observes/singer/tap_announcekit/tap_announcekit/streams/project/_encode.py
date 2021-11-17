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
from tap_announcekit.objs.project import (
    Project,
    ProjectObj,
)
from tap_announcekit.streams._obj_encoder import (
    encoder_1,
)
from typing import (
    Dict,
)


def _schema() -> JsonSchema:
    props = Project.__annotations__.copy()
    props["proj_id"] = str
    return encoder_1.to_jschema(props)


def _to_json(obj: ProjectObj) -> JsonObj:
    json: Dict[str, Primitive] = {
        "proj_id": obj.id_obj.id_str,
        "encoded_id": obj.obj.encoded_id,
        "name": obj.obj.name,
        "slug": obj.obj.slug,
        "website": obj.obj.website,
        "is_authors_listed": obj.obj.is_authors_listed,
        "is_whitelabel": obj.obj.is_whitelabel,
        "is_subscribable": obj.obj.is_subscribable,
        "is_slack_subscribable": obj.obj.is_slack_subscribable,
        "is_feedback_enabled": obj.obj.is_feedback_enabled,
        "is_demo": obj.obj.is_demo,
        "is_readonly": obj.obj.is_readonly,
        "image_id": obj.obj.image_id.id_str if obj.obj.image_id else None,
        "favicon_id": obj.obj.favicon_id.id_str
        if obj.obj.favicon_id
        else None,
        "created_at": obj.obj.created_at.isoformat(),
        "ga_property": obj.obj.ga_property,
        "avatar": obj.obj.avatar,
        "locale": obj.obj.locale,
        "uses_new_feed_hostname": obj.obj.uses_new_feed_hostname,
        "payment_gateway": obj.obj.payment_gateway,
        "trial_until": obj.obj.trial_until.isoformat()
        if obj.obj.trial_until
        else None,
        "metadata": obj.obj.metadata,
    }
    return JsonFactory.from_prim_dict(json)


@dataclass(frozen=True)
class ProjectEncoder:
    stream_name: str

    @property
    def schema(self) -> SingerSchema:
        p_keys = frozenset({"ext_user_id", "project_id"})
        return SingerSchema(self.stream_name, _schema(), p_keys)

    def to_singer(self, obj: ProjectObj) -> SingerRecord:
        return SingerRecord(self.stream_name, _to_json(obj))
