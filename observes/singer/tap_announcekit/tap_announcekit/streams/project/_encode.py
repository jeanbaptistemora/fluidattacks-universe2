# pylint: skip-file

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
    JsonValFactory,
    JsonValue,
    Primitive,
)
from singer_io.singer2.json_schema import (
    JsonSchema,
    JsonSchemaFactory,
    SupportedType,
)
from tap_announcekit.streams.project._objs import (
    ImageId,
    Project,
    ProjectId,
)
from typing import (
    Any,
    Dict,
    get_args,
    get_origin,
    Type,
    Union,
)


class UnexpectedType(Exception):
    pass


class UnsupportedMultipleType(Exception):
    pass


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


primitive_jschema_map = {
    bool: "boolean",
    float: "number",
    int: "integer",
    str: "string",
}


def _to_jschema(ptype: Type[Any]) -> JsonObj:
    if ptype in (ProjectId, ImageId):
        return JsonSchemaFactory.from_prim_type(str).to_json()
    elif ptype in (datetime,):
        return JsonSchemaFactory.datetime_schema().to_json()
    return JsonSchemaFactory.from_prim_type(ptype).to_json()


def _to_jschema_optional(ptype: Type[Any], optional: bool) -> JsonObj:
    jschema = _to_jschema(ptype).copy()
    if optional:
        jschema["type"] = JsonValFactory.from_list(
            [jschema["type"].to_primitive(str), SupportedType.null.value]
        )
    return jschema


def _to_jschema_type(ptype: Type[Any]) -> JsonObj:
    if get_origin(ptype) is Union:
        var_types = get_args(ptype)
        single_type = list(filter(lambda x: x != type(None), var_types))
        if len(single_type) > 1:
            raise UnsupportedMultipleType(single_type)
        return _to_jschema_optional(single_type[0], None in var_types)
    return _to_jschema_optional(ptype, False)


def _project_schema() -> JsonSchema:
    props = {
        key: JsonValue(_to_jschema_type(str_type))
        for key, str_type in Project.__annotations__.items()
    }
    return JsonSchemaFactory.from_json({"properties": JsonValue(props)})


@dataclass(frozen=True)
class ProjectEncoder:
    @staticmethod
    def to_json(project: Project) -> JsonObj:
        return _to_json(project)

    @staticmethod
    def schema() -> JsonSchema:
        return _project_schema()
