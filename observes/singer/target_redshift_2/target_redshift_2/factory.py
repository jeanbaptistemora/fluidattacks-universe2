"""Redshift* object factories"""
# Standard libraries
import re
from typing import (
    Any, Callable, Dict,
    FrozenSet,
    NamedTuple,
    Optional,
    Set,
    Tuple
)
# Third party libraries
# Local libraries
from target_redshift_2.db_client.objects import DbTypes
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftRecord,
    RedshiftSchema,
)
from target_redshift_2.singer import (
    SingerRecord,
    SingerSchema,
)


JSON_SCHEMA_TYPES: Dict[DbTypes, Any] = {
    DbTypes.BOOLEAN: [
        {"type": "boolean"},
        {"type": ["boolean", "null"]},
        {"type": ["null", "boolean"]}
    ],
    DbTypes.NUMERIC: [
        {"type": "integer"},
        {"type": ["integer", "null"]},
        {"type": ["null", "integer"]}
    ],
    DbTypes.FLOAT: [
        {"type": "number"},
        {"type": ["number", "null"]},
        {"type": ["null", "number"]}
    ],
    DbTypes.VARCHAR: [
        {"type": "string"},
        {"type": ["string", "null"]},
        {"type": ["null", "string"]}
    ],
    DbTypes.TIMESTAMP: [
        {"type": "string", "format": "date-time"},
        {
            "anyOf": [
                {"type": "string", "format": "date-time"},
                {"type": ["string", "null"]},
            ]
        },
        {
            "anyOf": [
                {"type": "string", "format": "date-time"},
                {"type": ["null", "string"]},
            ]
        }
    ]
}


class DbTypesFactory(NamedTuple):
    """Generator of `DbTypes` objects"""
    JSON_SCHEMA_TYPES: Dict[DbTypes, Any] = JSON_SCHEMA_TYPES

    def from_dict(
        self: 'DbTypesFactory', field_type: Dict[str, Any]
    ) -> Optional[DbTypes]:
        rtype: Optional[DbTypes] = None
        for redshift_type, json_schema_types in self.JSON_SCHEMA_TYPES.items():
            if field_type in json_schema_types:
                rtype = redshift_type
                break
        return rtype


class RedshiftSchemaFactory(NamedTuple):
    """Generator of `RedshiftSchema` objects"""
    # pylint: disable=too-many-function-args
    # required due to a bug with callable properties
    to_redshift_type: Callable[
        [Dict[str, Any]], Optional[DbTypes]
    ] = DbTypesFactory().from_dict

    def from_singer(
        self: 'RedshiftSchemaFactory',
        s_schema: SingerSchema,
        redshift_schema_name: str
    ) -> RedshiftSchema:
        """`SingerSchema` to `RedshiftSchema` transformation"""
        props = dict(s_schema.schema)['properties']
        fields: Set[RedshiftField] = set()
        for field, raw_type in props.items():
            s_type: Optional[DbTypes] = self.to_redshift_type(raw_type)
            if s_type:
                fields.add(RedshiftField(field, s_type))
            else:
                raise Exception(f'Unexpected type: {raw_type}')
        return RedshiftSchema(
            fields=frozenset(fields),
            schema_name=redshift_schema_name,
            table_name=s_schema.stream,
        )


def escape_fx(text: str) -> str:
    """
    Escape characters from an string object.
    Which are known to make a Redshift statement fail.
    """
    # remove null characters
    str_obj = re.sub("\x00", "", text)
    # backslash the backslash
    str_obj = str_obj.replace("\\", "\\\\")
    # escape double quotes for postgresql query
    str_obj = str_obj.replace('"', '""')
    # escape single quotes for postgresql query
    str_obj = str_obj.replace("'", "\\'")
    return str_obj


def str_len_fx(str_obj: str, encoding: str = "utf-8") -> int:
    """Returns the length in bytes of a string."""
    return len(str_obj.encode(encoding))


class RedshiftRecordFactory(NamedTuple):
    """Generator of `RedshiftRecord` objects"""
    # pylint: disable=too-many-function-args
    # required due to a bug with callable properties
    str_len: Callable[[str], int] = str_len_fx
    escape: Callable[[str], str] = escape_fx

    def from_singer(
        self: 'RedshiftRecordFactory',
        s_record: SingerRecord,
        r_schema: RedshiftSchema
    ) -> RedshiftRecord:
        """`SingerRecord` to `RedshiftRecord` transformation"""
        raw_record = dict(s_record.record)
        schema_fields: FrozenSet[str] = frozenset(
            map(lambda f: f.name, r_schema.fields)
        )
        new_field_val_pairs: Set[Tuple[str, str]] = set()
        field_type: Dict[str, DbTypes] = dict(r_schema.fields)
        for field, value in raw_record.items():
            if field in schema_fields:
                if field_type[field] == DbTypes.VARCHAR:
                    new_value = f"{value}"[0:256]
                    while self.str_len(self.escape(new_value)) > 256:
                        new_value = new_value[0:-1]
                    new_value = f"'{self.escape(new_value)}'"
                else:
                    new_value = f"'{self.escape(str(value))}'"
                new_field_val_pairs.add((field, new_value))
        return RedshiftRecord(
            r_schema=r_schema,
            record=frozenset(new_field_val_pairs)
        )
