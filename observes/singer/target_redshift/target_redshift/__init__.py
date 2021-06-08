# pylint: skip-file

"""Singer target for Amazon Redshift.

Examples:
    $ target-redshift --help
    $ tap-anysingertap | target-redshift [params]

Linters:
    prospector:
        Used always.
        $ prospector --strictness veryhigh [path]
    mypy:
        Used always.
        $ python3 -m mypy --ignore-missing-imports [path]
"""

import io
import json
import jsonschema
from postgres_client.client import (
    ClientFactory,
)
from postgres_client.schema import (
    SchemaFactory,
)
import psycopg2 as postgres
import sys
from target_redshift.batcher import (
    Batcher,
)
from target_redshift.utils import (
    escape,
    JSON,
    JSON_VALIDATOR,
    str_len,
)
from typing import (
    Any,
    Dict,
    IO,
    Iterable,
)
import utils_logger

utils_logger.configure(
    app_type="target",
    asynchronous=False,
)
LOG = utils_logger.main_log(__name__)


# Supported JSON Schema types
JSON_SCHEMA_TYPES: JSON = {
    "BOOLEAN": [
        {"type": "boolean"},
        {"type": ["boolean", "null"]},
        {"type": ["null", "boolean"]},
    ],
    "NUMERIC(38)": [
        {"type": "integer"},
        {"type": ["integer", "null"]},
        {"type": ["null", "integer"]},
    ],
    "FLOAT8": [
        {"type": "number"},
        {"type": ["number", "null"]},
        {"type": ["null", "number"]},
    ],
    "VARCHAR": [
        {"type": "string"},
        {"type": ["string", "null"]},
        {"type": ["null", "string"]},
    ],
    "TIMESTAMP": [
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
        },
    ],
}


def translate_schema(json_schema: JSON) -> Dict[str, str]:
    """Translates a JSON schema into a Redshift schema.

    Whenever the type is not supported, it is discarded.

    Args:
        json_schema: A JSON with the JSON schema.

    Raises:
        Warnings when the type is not supported.

    Returns:
        A JSON representing a Redshift schema.

    Examples:
        >>> json_schema = {"field": {"type": "string", "format": "date-time"}}
        >>> translate_schema(json_schema)
        {"field": "TIMESTAMP"}

        >>> json_schema = {"fie'ld": {"type": "string", "format": "date-time"}}
        >>> translate_schema(json_schema)
        {"fie\'ld": "TIMESTAMP"}

        >>> json_schema = {"other_field": {"type": "unknown_type"}}
        >>> translate_schema(json_schema)
        {}
    """

    def stor(stype: JSON) -> str:
        """Translates a Singer data type into a Redshift data type.

        Args:
            json_schema: A dict with the json schema data type.

        Returns:
            A string representing a Redshift data type.
        """
        rtype = ""
        for redshift_type, json_schema_types in JSON_SCHEMA_TYPES.items():
            if stype in json_schema_types:
                rtype = redshift_type
                break
        else:
            LOG.warning(
                (
                    "WARN: Ignoring type %s, "
                    "it's not supported by the target (yet)."
                ),
                stype,
            )
        return rtype

    return {escape(f): stor(st) for f, st in json_schema.items() if stor(st)}


def translate_record(schema: JSON, record: JSON) -> Dict[str, str]:
    """Translates a JSON record into a Redshift JSON.

    Whenever the type is not supported, its value is discarded.
    Whenever a field is provieded but it's not in the schema, it's discarded.

    Args:
        schema: A JSON with the JSON schema.
        record: A JSON with the JSON record.

    Raises:
        Warnings when the type is not supported or extra fields are provided.

    Returns:
        A JSON representing a Redshift record compatible with the schema.

    Examples:
        >>> schema = {"field": {"type": "number"}}
        >>> record = {"field": 2.48}
        >>> translate_record(schema, record)
        {"field": 2.48}

        >>> schema = {"field": {"type": "number"}}
        >>> record = {"extra_field": "example"}
        >>> translate_record(schema, record)
        WARN: Ignoring field extra_field, it's not in the streamed schema.
        {}
    """

    new_record = {}
    for user_field, user_value in record.items():
        new_field = escape(user_field)
        new_value = ""
        if new_field not in schema:
            LOG.warning(
                (
                    "WARN: Ignoring field %s, "
                    "it's not in the streamed schema."
                ),
                new_field,
            )
        elif user_value is not None:
            new_field_type = schema[new_field]
            if new_field_type == "BOOLEAN":
                new_value = f"{escape(user_value).lower()}"
            elif new_field_type == "NUMERIC(38)":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "FLOAT8":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "VARCHAR":
                new_value = f"{user_value}"[0:256]
                while str_len(escape(new_value)) > 256:
                    new_value = new_value[0:-1]
                new_value = f"'{escape(new_value)}'"
            elif new_field_type == "TIMESTAMP":
                new_value = f"'{escape(user_value)}'"
            else:
                LOG.warning(
                    (
                        "WARN: Ignoring type %s, "
                        "it's not in the streamed schema."
                    ),
                    new_field_type,
                )

            new_record[new_field] = new_value
    return new_record


def create_schema(batcher: Batcher, schema_name: str) -> None:
    """Creates the schema unless it currently exist.

    Args:
        batcher: The query executor.
        schema_name: The schema to operate over.
    """
    try:
        batcher.ex(f'CREATE SCHEMA "{schema_name}"', True)
    except postgres.ProgrammingError as exc:
        LOG.error("EXCEPTION: %s %s", type(exc), exc)


def create_table(
    batcher: Batcher,
    schema_name: str,
    table_name: str,
    table_types: Dict[str, str],
    table_pkeys: Iterable[str],
) -> None:
    """Creates a table in the schema unless it currently exist.

    If the table exists in the schema, it leave it unchanged.

    Args:
        batcher: The query executor.
        schema_name: The schema to operate over.
        table_fields: The table field names.
        table_types: The table {field: type}.
        table_pkeys: The table primary keys.
    """
    # pylint: disable=too-many-arguments
    table_fields = batcher.fields[table_name]

    path = f'"{schema_name}"."{table_name}"'
    fields = ",".join([f'"{n}" {table_types[n]}' for n in table_fields])

    try:
        if table_pkeys:
            pkeys = ",".join([f'"{n}"' for n in table_pkeys])
            batcher.ex(f"CREATE TABLE {path} ({fields},PRIMARY KEY({pkeys}))")
        else:
            batcher.ex(f"CREATE TABLE {path} ({fields})")
    except postgres.ProgrammingError as exc:
        LOG.error("EXCEPTION: %s %s", type(exc), exc)


def rename_schema(batcher: Batcher, rename_from: str, rename_to: str) -> None:
    """Renames the schema.

    It leaves the schema untouched if rename_from don't exist.
    It leaves the schema untouched if rename_to currently exist.

    If the table exists in the schema, it leave it unchanged.

    Args:
        batcher: The query executor.
        rename_from: The schema you wish to rename.
        rename_to: The schema you wish your schema to be renamed to.
    """
    try:
        statement = f'ALTER SCHEMA "{rename_from}" RENAME TO "{rename_to}"'
        batcher.ex(statement, True)
    except postgres.ProgrammingError as exc:
        LOG.error("EXCEPTION: %s %s", type(exc), exc)


def validate_schema(validator: JSON_VALIDATOR, schema: JSON) -> None:
    """Prints the validation of a JSON by using the provided validator."""

    try:
        validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as err:
        LOG.critical("ERROR: schema did not conform to draft 4.")
        LOG.critical(err)
        sys.exit(1)


def validate_record(validator: JSON_VALIDATOR, record: JSON) -> None:
    """Prints the validation of a JSON by using the provided validator."""

    try:
        validator.validate(record)
    except jsonschema.exceptions.ValidationError as err:
        LOG.warning("WARN: record did not conform to schema.")
        LOG.warning(err)


def persist_messages(batcher: Batcher, schema_name: str) -> None:
    """Persist messages received in stdin to Amazon Redshift.

    Args:
        batcher: The query executor.
        schema_name: The schema to operate over.
    """
    schemas: Dict[str, Dict[str, str]] = {}
    validators: Any = {}

    for message in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
        try:
            json_obj: JSON = json.loads(message)
        except json.JSONDecodeError:
            continue
        if json_obj["type"] == "RECORD":
            tname: str = escape(json_obj["stream"].lower())
            tschema: JSON = schemas[tname]

            json_record: JSON = json_obj["record"]
            validate_record(validators[tname], json_record)

            record: Dict[str, str] = translate_record(tschema, json_record)

            batcher.queue(tname, record)
        elif json_obj["type"] == "SCHEMA":
            tname = escape(json_obj["stream"].lower())
            tkeys = tuple(map(escape, json_obj["key_properties"]))
            tschema = json_obj["schema"]

            validators[tname] = jsonschema.Draft4Validator(tschema)
            validate_schema(validators[tname], tschema)

            schemas[tname] = translate_schema(tschema["properties"])

            batcher.set_field_names(tname, list(schemas[tname].keys()))

            create_table(batcher, schema_name, tname, schemas[tname], tkeys)
        elif json_obj["type"] == "STATE":
            LOG.info(json.dumps(json_obj, indent=2))

    batcher.flush()
    batcher.vacuum()


def main(auth_file: IO[str], schema_name: str, drop_schema_flag: bool) -> None:
    """Usual entry point."""

    greeting = (
        "                                   ",
        " Singer target for Amazon Redshift ",
        "                                   ",
        "            ___                    ",
        "           | >>|> fluid            ",
        "           |___|  attacks          ",
        "                                   ",
        "       We hack your software       ",
        "                                   ",
        "     https://fluidattacks.com/     ",
        "                                   ",
    )

    LOG.info("\n".join(greeting))

    target_schema = schema_name
    backup_schema = f"{target_schema}_backup"
    loading_schema = f"{target_schema}_loading"

    factory = ClientFactory()
    client = factory.from_conf(auth_file)
    schema_factory = SchemaFactory(client)

    try:
        dbcur = client.cursor.db_cursor

        if drop_schema_flag:
            # It means user wants to guarantee 100% data integrity
            # It also implies the use of a loading strategy
            #   to guarantee continuated service availability

            batcher = Batcher(dbcur, loading_schema)

            # The loading strategy is:
            #   DROP loading_schema
            schema_factory.try_retrieve(loading_schema).map(
                lambda schema: schema_factory.delete(schema, cascade=True)
            )
            #   MAKE loading_schema
            create_schema(batcher, loading_schema)
            #   LOAD loading_schema
            persist_messages(batcher, loading_schema)
            #   DROP backup_schema IF EXISTS
            schema_factory.try_retrieve(backup_schema).map(
                lambda schema: schema_factory.delete(schema, cascade=True)
            )
            #   REN  target_schema TO backup_schema
            rename_schema(batcher, target_schema, backup_schema)
            #   REN  loading_schema TO target_schema
            rename_schema(batcher, loading_schema, target_schema)
        else:
            # It means user only wants to push data and
            #   just cares about having it there.
            # The trade-off is:
            #     - data integrity
            #     - possible un-updated schema
            #     - and dangling/orphan/duplicated records
            batcher = Batcher(dbcur, target_schema)
            persist_messages(batcher, target_schema)
    finally:
        client.close()
