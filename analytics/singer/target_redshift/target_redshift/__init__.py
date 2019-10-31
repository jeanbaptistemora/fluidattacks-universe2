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
import re
import sys
import json
import time
import logging
import argparse

from datetime import datetime
from typing import Iterable, Dict, List, Tuple, Any

import jsonschema
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions

# Type aliases that improve clarity
JSON = Any
PGCONN = Any
PGCURR = Any
JSON_VALIDATOR = Any

# Get us a logger prepared to stdout
LOGGER: Any = logging.getLogger("target_redshift")
STDOUT: Any = logging.StreamHandler()
LOGGER.setLevel(logging.INFO)
STDOUT.setLevel(logging.INFO)
LOGGER.addHandler(STDOUT)

# Supported JSON Schema types
JSON_SCHEMA_TYPES: JSON = {
    "BOOLEAN": [
        {
            "type": "boolean"
        },
        {
            "type": [
                "boolean",
                "null"
            ]
        },
        {
            "type": [
                "null",
                "boolean"
            ]
        }
    ],
    "INT8": [
        {
            "type": "integer"
        },
        {
            "type": [
                "integer",
                "null"
            ]
        },
        {
            "type": [
                "null",
                "integer"
            ]
        }
    ],
    "FLOAT8": [
        {
            "type": "number"
        },
        {
            "type": [
                "number",
                "null"
            ]
        },
        {
            "type": [
                "null",
                "number"
            ]
        }
    ],
    "VARCHAR": [
        {
            "type": "string"
        },
        {
            "type": [
                "string",
                "null"
            ]
        },
        {
            "type": [
                "null",
                "string"
            ]
        }
    ],
    "TIMESTAMP": [
        {
            "type": "string",
            "format": "date-time"
        },
        {
            "anyOf": [
                {
                    "type": "string",
                    "format": "date-time"
                },
                {
                    "type": [
                        "string",
                        "null"
                    ]
                },
            ]
        },
        {
            "anyOf": [
                {
                    "type": "string",
                    "format": "date-time"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ]
                },
            ]
        }
    ]
}

# pylint: disable = logging-fstring-interpolation


def str_len(str_obj: str, encoding: str = "utf-8") -> int:
    """Returns the length in bytes of a string.

    Args:
        str_obj: the string to compute its length.

    Returns:
        The length in bytes of the string.
    """
    return len(str_obj.encode(encoding))


def stringify(iterable: Iterable[Any], do_group: bool = True) -> str:
    """Returns a string representation of an iterable.

    Args:
        iterable: The iterable to process.
        do_group: True if you want to enclose elements with parentheses.

    Returns:
        A string representation of the iterable.

    Examples:
        >>> iterable = tuple(1, 2, 3)
        >>> stringify(iterable, do_group=False)
        "1,2,3"
        >>> stringify(iterable, do_group=True)
        "(1),(2),(3)"
    """

    if do_group:
        return ",".join(f"({x})" for x in iterable)
    return ",".join(f"{x}" for x in iterable)


def make_access_point(auth: Dict[str, str]) -> Tuple[PGCONN, PGCURR]:
    """Returns a connection and a cursor to the database.

    It sets the connection to allow write operations.
    It sets the isolation level to auto-commit.

    Args:
        auth: A dictionary with the authentication parameters.

    Returns:
        A tuple with a connection and a cursor to the database.
    """

    dbcon: PGCONN = postgres.connect(
        dbname=auth["dbname"],
        user=auth["user"],
        password=auth["password"],
        host=auth["host"],
        port=auth["port"]
    )

    dbcon.set_session(readonly=False)
    dbcon.set_isolation_level(postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    dbcur: PGCURR = dbcon.cursor()

    return (dbcon, dbcur)


def drop_access_point(dbcon: PGCONN, dbcur: PGCURR) -> None:
    """Safely close the access point.

    Args:
        dbcon: The database connection.
        dbcur: The database cursor.
    """
    dbcur.close()
    dbcon.close()


def escape(obj: str) -> str:
    """Escape characters from an string object.

    It makes the object decay to an string, if not yet string.
    It removes null byte characters.
    It backslash the backslash, apostrophe, and quotation mark characters.

    Which are known to make a Redshift statement fail.

    Args:
        str_obj: The string to escape.

    Returns:
        A escaped string.
    """

    # decay to string if not yet string
    str_obj = str(obj)

    # remove null characters
    str_obj = re.sub("\x00", "", str_obj)

    # backslash the backslash
    str_obj = str_obj.replace("\\", "\\\\")

    # backslash the apostrophe and quotation mark
    for char in ("'", '"'):
        str_obj = re.sub(char, f"\\{char}", str_obj)

    return str_obj


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
            LOGGER.warning((f"WARN: Ignoring type {stype}, "
                            f"it's not supported by the target (yet)."))
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
            LOGGER.warning((f"WARN: Ignoring field {new_field}, "
                            f"it's not in the streamed schema."))
        elif user_value is not None:
            new_field_type = schema[new_field]
            if new_field_type == "BOOLEAN":
                new_value = f"{escape(user_value).lower()}"
            elif new_field_type == "INT8":
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
                LOGGER.warning((f"WARN: Ignoring type {new_field_type}, "
                                f"it's not in the streamed schema."))

            new_record[new_field] = new_value
    return new_record


class Batcher():
    """A class that wraps a Redshift query executor.

    Args:
        dbcon: The database connection.
        dbcur: The database cursor.
        schema_name: The schema to operate over.

    Attributes:
        initt: Class's instantiation timestamp.
        dbcon: The database connection.
        dbcur: The database cursor.
        sname: Schema name over which the Class is operating.
        buckets: An object that stores the queued statements.

    Public methods:
        ex: Executes a statement on the database.
        queue: Queue a row to be loaded into a table.
        load: Loads a batch of queued rows into a table.
        flush: Loads batches queued for all tables.
        vacuum: Vacuums loaded tables to improve query performance.

    Raises:
        postgres.ProgrammingError: When a query was corrupted.
        Status information from time to time.
    """

    def __init__(self, dbcur: PGCURR, schema_name: str) -> None:
        LOGGER.info(f"INFO: worker up at {datetime.utcnow()}.")

        self.initt: float = time.time()

        self.dbcur: PGCURR = dbcur

        self.msize: int = 0

        self.sname: str = schema_name
        self.buckets: Dict[str, Any] = {}

    def ex(self, statement: str, do_print: bool = False) -> None:
        """Executes a single statement.

        Args:
            statement: Statement to be run.
            do_print: True if you want to print the statement to stdout.

        Raises:
            postgres.ProgrammingError: When a query was corrupted.
        """
        if do_print:
            LOGGER.info(f"EXEC: {statement}.")
        self.dbcur.execute(statement)

    def queue(self, table_name: str, values: List[str]) -> None:
        """Queue rows in buckets before pushing them to redshift.

        All values must come here as a string representation.
            see translate_record().
        Values are stored in a bucket as a list of rows.
            a row is a string of its values separated by comma.
        Buckets are automatically loaded when they reach the optimal size.

        Args:
            table_name: Table that owns the rows.
            values: The row's values to be load.
        """

        # initialize the bucket
        if table_name not in self.buckets:
            self.buckets[table_name] = {
                "rows": [],
                "count": 0,
                "size": 0
            }

        # turn a row into a string of values separated by comma
        row = stringify(values, do_group=False)
        row_size = str_len(row)

        # a redshift statement must be less than 16MB, save 1KB for the header

        # if we are to exceed the limit with the current row
        if self.buckets[table_name]["size"] + row_size >= 15999000:
            # load the queued rows to Redshift
            self.load(table_name)

        if self.msize >= 256 * 1024 * 1024:
            self.flush()

        # queues the provided row in this function call
        self.msize += row_size
        self.buckets[table_name]["rows"].append(row)
        self.buckets[table_name]["count"] += 1
        self.buckets[table_name]["size"] += row_size

    def load(self, table_name: str, do_print: bool = False) -> None:
        """Loads a batch of queued rows to redshift.

        Args:
            table_name: Table that owns the rows.
            do_print: True if you want to print the statement to stdout.
        """

        # take every comma separated string, and surround it with parenthesis
        values = stringify(self.buckets[table_name]["rows"], do_group=True)

        statement = f"""
            INSERT INTO \"{self.sname}\".\"{table_name}\"
            VALUES {values}"""
        self.ex(statement, do_print)

        count = self.buckets[table_name]["count"]
        size = round(self.buckets[table_name]["size"] / 1.0e6, 2)
        LOGGER.info((f"INFO: {count} rows ({size} MB) "
                     f"loaded to Redshift/{self.sname}/{table_name}."))

        self.msize -= self.buckets[table_name]["size"]
        self.buckets[table_name]["rows"] = []
        self.buckets[table_name]["count"] = 0
        self.buckets[table_name]["size"] = 0

    def flush(self, do_print: bool = False) -> None:
        """Loads to redshift the buckets that din't reach the optimal size.

        Args:
            do_print: True if you want to print the statements to stdout.
        """
        for table_name in self.buckets:
            self.load(table_name, do_print)
        self.msize = 0

    def vacuum(self, do_print: bool = True) -> None:
        """Vacuums touched tables to improve query performance.

        Args:
            do_print: True if you want to print the statements to stdout.
        """
        vacuum_errors = (
            postgres.ProgrammingError,
            postgres.NotSupportedError,
        )
        for table_name in self.buckets:
            try:
                table_path: str = f"\"{self.sname}\".\"{table_name}\""
                self.ex(
                    f"VACUUM FULL {table_path} TO 100 PERCENT",
                    do_print=do_print)
            except vacuum_errors:
                LOGGER.info(f"INFO: unable to vacuum \"{table_name}\"")

    def __del__(self, *args) -> None:
        LOGGER.info(f"INFO: worker down at {datetime.utcnow()}.")
        LOGGER.info(f"INFO: {time.time() - self.initt} seconds elapsed.")


def drop_schema(batcher: Batcher, schema_name: str) -> None:
    """Drop the schema unless it doesn't exist.

    Args:
        batcher: The query executor.
        schema_name: The schema to operate over.
    """

    try:
        batcher.ex(f"DROP SCHEMA \"{schema_name}\" CASCADE", True)
    except postgres.ProgrammingError as exc:
        LOGGER.error(f'EXCEPTION: {type(exc)} {exc}')


def create_schema(batcher: Batcher, schema_name: str) -> None:
    """Creates the schema unless it currently exist.

    Args:
        batcher: The query executor.
        schema_name: The schema to operate over.
    """
    try:
        batcher.ex(f"CREATE SCHEMA \"{schema_name}\"", True)
    except postgres.ProgrammingError as exc:
        LOGGER.error(f'EXCEPTION: {type(exc)} {exc}')


def create_table(
        batcher: Batcher,
        schema_name: str, table_name: str,
        table_fields: Iterable[str],
        table_types: Dict[str, str],
        table_pkeys: Iterable[str]) -> None:
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

    path = f"\"{schema_name}\".\"{table_name}\""
    fields = ",".join([f"\"{n}\" {table_types[n]}" for n in table_fields])

    try:
        if table_pkeys:
            pkeys = ",".join([f"\"{n}\"" for n in table_pkeys])
            batcher.ex(f"CREATE TABLE {path} ({fields},PRIMARY KEY({pkeys}))")
        else:
            batcher.ex(f"CREATE TABLE {path} ({fields})")
    except postgres.ProgrammingError as exc:
        LOGGER.error(f'EXCEPTION: {type(exc)} {exc}')


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
        statement = f"ALTER SCHEMA \"{rename_from}\" RENAME TO \"{rename_to}\""
        batcher.ex(statement, True)
    except postgres.ProgrammingError as exc:
        LOGGER.error(f'EXCEPTION: {type(exc)} {exc}')


def validate_schema(validator: JSON_VALIDATOR, schema: JSON) -> None:
    """Prints the validation of a JSON by using the provided validator.
    """

    try:
        validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as err:
        LOGGER.critical(f"ERROR: schema did not conform to draft 4.")
        LOGGER.critical(err)
        exit(1)


def validate_record(validator: JSON_VALIDATOR, record: JSON) -> None:
    """Prints the validation of a JSON by using the provided validator.
    """

    try:
        validator.validate(record)
    except jsonschema.exceptions.ValidationError as err:
        LOGGER.warning(f"WARN: record did not conform to schema.")
        LOGGER.warning(err)


def persist_messages(batcher: Batcher, schema_name: str) -> None:
    """Persist messages received in stdin to Amazon Redshift.

    Args:
        batcher: The query executor.
        schema_name: The schema to operate over.
    """

    fields: JSON = {}
    schemas: JSON = {}
    validators: Any = {}

    for message in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
        json_obj: JSON = json.loads(message)
        if json_obj["type"] == "RECORD":
            tname: str = escape(json_obj["stream"].lower())
            tschema: JSON = schemas[tname]
            tfields: Iterable = fields[tname]

            json_record: JSON = json_obj["record"]
            validate_record(validators[tname], json_record)

            record: Dict[str, str] = translate_record(tschema, json_record)

            record_ov: List[str] = []
            for field in tfields:
                try:
                    record_ov.append(record[field])
                except KeyError:
                    record_ov.append("null")

            batcher.queue(tname, record_ov)
        elif json_obj["type"] == "SCHEMA":
            tname = escape(json_obj["stream"].lower())
            tkeys = tuple(map(escape, json_obj["key_properties"]))
            tschema = json_obj["schema"]

            validators[tname] = jsonschema.Draft4Validator(tschema)
            validate_schema(validators[tname], tschema)

            schemas[tname] = translate_schema(tschema["properties"])
            fields[tname] = tuple(schemas[tname].keys())

            create_table(
                batcher, schema_name, tname,
                fields[tname], schemas[tname], tkeys)
        elif json_obj["type"] == "STATE":
            LOGGER.info(json.dumps(json_obj, indent=2))

    batcher.flush()
    batcher.vacuum()


def main():
    """Usual entry point.
    """

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
        "                                   "
    )

    LOGGER.info("\n".join(greeting))

    # user interface
    parser = argparse.ArgumentParser(
        description="Persists a singer formatted stream to Amazon Redsfhit")
    parser.add_argument(
        "-a", "--auth",
        required=True,
        help="JSON authentication file",
        type=argparse.FileType("r"),
        dest="auth")
    parser.add_argument(
        "-s", "--schema-name",
        required=True,
        help="Schema name in your warehouse",
        dest="schema_name")
    parser.add_argument(
        "-ds", "--drop-schema",
        required=False,
        help="Flag to specify that you want to delete the schema if exist",
        action="store_true",
        dest="drop_schema",
        default=False)

    args = parser.parse_args()
    auth = json.load(args.auth)

    target_schema = f"{args.schema_name}"
    backup_schema = f"{target_schema}_backup"
    loading_schema = f"{target_schema}_loading"

    try:
        (dbcon, dbcur) = make_access_point(auth)

        if args.drop_schema:
            # It means user wants to guarantee 100% data integrity
            # It also implies the use of a loading strategy
            #   to guarantee continuated service availability

            batcher = Batcher(dbcur, loading_schema)

            # The loading strategy is:
            #   DROP loading_schema
            drop_schema(batcher, loading_schema)
            #   MAKE loading_schema
            create_schema(batcher, loading_schema)
            #   LOAD loading_schema
            persist_messages(batcher, loading_schema)
            #   DROP backup_schema IF EXISTS
            drop_schema(batcher, backup_schema)
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
        drop_access_point(dbcon, dbcur)


if __name__ == "__main__":
    main()
