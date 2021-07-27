# pylint: skip-file

from returns.maybe import (
    Maybe,
)
from singer_io.singer2._objs import (
    SingerSchema,
)
from singer_io.singer2.json import (
    DictFactory,
    JsonFactory,
)
from singer_io.singer2.json_schema import (
    JsonSchemaFactory,
)


class MissingKeys(Exception):
    pass


class InvalidType(Exception):
    pass


def deserialize_schema(raw_singer_schema: str) -> SingerSchema:
    """Generate `SingerSchema` from json string"""
    raw_dict = DictFactory.loads(raw_singer_schema)
    raw_json = JsonFactory.from_dict(raw_dict)
    required_keys = frozenset({"type", "stream", "schema", "key_properties"})
    invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
    if invalid:
        raise MissingKeys("Can not generate `SingerSchema` object")
    parsed_type = raw_json["type"].to_primitive(str)
    if parsed_type == "SCHEMA":
        bookmark_properties = (
            Maybe.from_optional(raw_json.get("bookmark_properties", None))
            .map(lambda item: item.to_list_of(str))
            .map(lambda item: frozenset(item))
        )
        return SingerSchema(
            stream=raw_json["stream"].to_primitive(str),
            schema=JsonSchemaFactory.from_dict(raw_dict),
            key_properties=frozenset(
                raw_json["key_properties"].to_list_of(str)
            ),
            bookmark_properties=bookmark_properties.value_or(None),
        )
    raise InvalidType(f'Expected "SCHEMA" not "{parsed_type}"')
