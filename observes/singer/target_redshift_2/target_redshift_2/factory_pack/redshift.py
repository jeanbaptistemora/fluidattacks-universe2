# Standard libraries
import re
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    NamedTuple,
    Optional,
    Set,
    Tuple
)
# Third party libraries
# Local libraries
from postgres_client.table import DbTypes
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from target_redshift_2.utils import Transform
from target_redshift_2.objects import (
    InvalidType, RedshiftField,
    RedshiftRecord,
    RedshiftSchema,
)


class RedshiftElementsFactory(NamedTuple):
    """Generator of `RedshiftSchema` objects"""
    to_rschema: Callable[[SingerSchema], RedshiftSchema]
    to_rrecord: Callable[[SingerSchema], RedshiftSchema]


def singer_to_rschema(
    s_schema: SingerSchema,
    redshift_schema_name: str,
    to_db_type: Transform[Dict[str, Any], Optional[DbTypes]]
) -> RedshiftSchema:
    """`SingerSchema` to `RedshiftSchema` transformation"""
    props = dict(s_schema.schema)['properties']
    fields: Set[RedshiftField] = set()
    for field, raw_type in props.items():
        s_type: Optional[DbTypes] = to_db_type(raw_type)
        if s_type:
            fields.add(RedshiftField(field, s_type))
        else:
            raise InvalidType(f'type: {raw_type} not supported')
    return RedshiftSchema(
        fields=frozenset(fields),
        schema_name=redshift_schema_name,
        table_name=s_schema.stream,
    )


def escape(text: str) -> str:
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


def str_len(str_obj: str, encoding: str = "utf-8") -> int:
    """Returns the length in bytes of a string."""
    return len(str_obj.encode(encoding))


def singer_to_rrecord(
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
                while str_len(escape(new_value)) > 256:
                    new_value = new_value[0:-1]
                new_value = f"'{escape(new_value)}'"
            else:
                new_value = f"'{escape(str(value))}'"
            new_field_val_pairs.add((field, new_value))
    return RedshiftRecord(
        r_schema=r_schema,
        record=frozenset(new_field_val_pairs)
    )
