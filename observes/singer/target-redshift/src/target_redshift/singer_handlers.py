import json
import jsonschema
import logging
from postgres_client.column import (
    RedshiftDataType,
)
from postgres_client.table import (
    TableFactory,
)
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
    SingerState,
)
from target_redshift.batcher import (
    Batcher,
)
from target_redshift.data_schema import (
    RedshiftSchema,
)
from target_redshift.utils import (
    escape,
    str_len,
)
from tempfile import (
    TemporaryFile,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)

LOG = logging.getLogger(__name__)
SchemasMap = Dict[str, RedshiftSchema]


def _escape_value(r_type: RedshiftDataType, value: Any) -> str:
    new_value = ""
    if r_type == RedshiftDataType.BOOLEAN:
        new_value = f"{escape(value).lower()}"
    elif r_type in (
        RedshiftDataType.INTEGER,
        RedshiftDataType.DOUBLE_PRECISION,
    ):
        new_value = f"{escape(value)}"
    elif r_type == RedshiftDataType.VARCHAR:
        new_value = f"{value}"[0:256]
        while str_len(escape(new_value)) > 256:
            new_value = new_value[0:-1]
        new_value = f"'{escape(new_value)}'"
    elif r_type == RedshiftDataType.TIMESTAMP:
        new_value = f"'{escape(value)}'"
    else:
        LOG.warning(
            ("WARN: Ignoring type %s, it's not in the streamed schema."),
            r_type,
        )
    return new_value


def _translate_record(
    r_schema: RedshiftSchema, s_record: SingerRecord
) -> Dict[str, str]:
    field_type_map = r_schema.table.field_type_map()
    new_record = {}
    for field, value in s_record.record.items():
        escaped_field = escape(field).lower()
        if escaped_field not in field_type_map.keys():
            LOG.warning(
                (
                    "WARN: Ignoring field %s, "
                    "it's not in the streamed schema."
                ),
                escaped_field,
            )
        elif value is not None:
            new_record[escaped_field] = _escape_value(
                field_type_map[escaped_field].field_type, value
            )
    return new_record


def _validate_record(r_schema: RedshiftSchema, s_record: SingerRecord) -> None:
    try:
        r_schema.validator.validate(s_record.record)
    except jsonschema.exceptions.ValidationError as err:
        LOG.warning("WARN: record did not conform to schema.")
        LOG.warning(err)


def record_handler(
    batcher: Batcher,
    s_record: SingerRecord,
    schemas: SchemasMap,
) -> SchemasMap:
    tname: str = escape(s_record.stream.lower())
    r_schema = schemas[tname]
    _validate_record(r_schema, s_record)
    record: Dict[str, str] = _translate_record(r_schema, s_record)
    batcher.queue(tname, record)
    return schemas


# pylint: disable=too-many-arguments
def schema_handler(
    batcher: Batcher,
    table_factory: TableFactory,
    update_table: bool,
    db_schema: str,
    s_schema: SingerSchema,
    schemas: SchemasMap,
) -> SchemasMap:
    r_schema = RedshiftSchema(db_schema, s_schema)
    modified_map = False
    schemas_map = schemas.copy()
    tname = r_schema.table.table_id.table_name
    if tname not in schemas_map:
        schemas_map[tname] = r_schema
        modified_map = True

    batcher.set_field_names(
        tname, list(map(lambda col: col.name, r_schema.table.columns))
    )
    table_io = table_factory.new_table(r_schema.table, True)
    if update_table:
        table_io.map(lambda table: table.add_columns(r_schema.table.columns))
    if not modified_map:
        return schemas
    return schemas_map


class StateId(NamedTuple):
    bucket: str
    obj_key: str


def state_handler(
    s3_client: Any,
    state_id: Optional[StateId],
    s_state: SingerState,
    schemas: SchemasMap,
) -> SchemasMap:
    if state_id:
        LOG.info("Uploading new state")
        LOG.debug("Uploading state to %s", state_id)
        with TemporaryFile() as data:
            data.write(
                bytes(json.dumps(s_state.value, indent=4).encode("UTF-8"))
            )
            data.seek(0)
            s3_client.upload_fileobj(data, state_id.bucket, state_id.obj_key)
    return schemas
