from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
    Primitive,
)
from tap_announcekit.stream.project._objs import (
    Project,
)
from typing import (
    Dict,
)


def to_json(proj: Project) -> JsonObj:
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
        "image_id": proj.image_id,
        "favicon_id": proj.favicon_id,
        "created_at": proj.created_at.isoformat(),
        "ga_property": proj.ga_property,
        "avatar": proj.avatar,
        "favicon": proj.favicon,
        "locale": proj.locale,
        "uses_new_feed_hostname": proj.uses_new_feed_hostname,
        "payment_gateway": proj.payment_gateway,
        "trial_until": proj.trial_until.isoformat()
        if proj.trial_until
        else None,
        "metadata": proj.metadata,
    }
    return JsonFactory.from_prim_dict(json)
