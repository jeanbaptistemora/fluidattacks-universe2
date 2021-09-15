# pylint: skip-file

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from returns.maybe import (
    Maybe,
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


def _type_jschema_map(ptype: Type[Any], optional: bool) -> JsonObj:
    extended_map = primitive_jschema_map.copy()
    extended_map[ProjectId] = "string"
    extended_map[ImageId] = "string"
    extended_map[datetime] = "string"
    schema_type = Maybe.from_optional(extended_map.get(ptype)).map(
        lambda x: JsonValFactory.from_list([x, "null"])
        if optional
        else JsonValue(x)
    )
    if schema_type.value_or(None):
        if ptype == datetime:
            return {
                "type": schema_type.unwrap(),
                "format": JsonValue("date-time"),
            }
        return {"type": schema_type.unwrap()}
    raise UnexpectedType(f"{ptype} {type(ptype)}")


def _to_jschema_type(ptype: Type[Any]) -> JsonObj:
    if get_origin(ptype) is Union:
        var_types = get_args(ptype)
        single_type = list(filter(lambda x: x != type(None), var_types))
        if len(single_type) > 1:
            raise UnsupportedMultipleType(single_type)
        return _type_jschema_map(single_type[0], None in var_types)
    return _type_jschema_map(ptype, False)


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
