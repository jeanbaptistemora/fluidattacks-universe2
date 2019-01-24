"""Singer target for Amazon Redshift.

Example:
    $ tap-anysingertap | target-redshift [params]

Linters:
    pylint:
        Used always.
        $ python3 -m pylint [path]
    flake8:
        Used always except where it contradicts pylint.
        $ python3 -m flake8 [path]
    mypy:
        Used always.
        $ python3 -m mypy --ignore-missing-imports [path]
"""

import io
import re
import sys
import json
import time
import argparse

from datetime import datetime
from typing import Iterable, Dict, Any

# pylint: disable=import-error
import jsonschema
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions


def identity(obj: Any) -> Any:
    """Takes a single argument and returns it unchanged.

    Args:
        obj: any single argument.

    Returns:
        obj: exactly as it was provided.
    """
    return obj


def str_len(str_obj: str, encoding: str = "utf-8") -> int:
    """Returns the length in bytes of a string.

    Args:
        str_obj: the string to compute its length.

    Returns:
        The length in byes of the string.
    """
    return len(str_obj.encode(encoding))


def stringify(iterable: Iterable[Any], do_group: bool = True) -> str:
    """Returns a string representation of an iterable.

    Args:
        iterable: The iterable to process.
        do_group: True if you want to enclose elements with parens.

    Returns:
        A string representation of the iterable

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


def make_access_point(auth: Dict[str, str]):
    """Returns a connection and a cursor to the database.

    It sets the connection to allow write operations.
    It sets the isolation level to auto-commit.

    Args:
        auth: A dictionary with the authentication parameters.

    Returns:
        A tuple with a connection and a cursor to the database.
    """

    dbcon = postgres.connect(
        dbname=auth["dbname"],
        user=auth["user"],
        password=auth["password"],
        host=auth["host"],
        port=auth["port"]
    )

    dbcon.set_session(readonly=False)
    dbcon.set_isolation_level(postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    dbcur = dbcon.cursor()

    return (dbcon, dbcur)


def drop_access_point(dbcon, dbcur) -> None:
    """Safely close the access point.

    Args:
        dbcon: The database connection.
        dbcur: The database cursor.
    """
    dbcur.close()
    dbcon.close()


def escape(obj: Any) -> str:
    """Escape characters from an string object.

    It makes the object decay to an string, if not string.
    It removes null byte characters.
    It backslash the backslash, apostrophe, and quotation mark characters.

    Args:
        str_obj: The string to escape.

    Returns:
        A escaped string.
    """

    str_obj = str(obj)
    str_obj = re.sub("\x00", "", str_obj)
    str_obj = str_obj.replace("\\", "\\\\")

    for char in ("'", '"'):
        str_obj = re.sub(char, f"\\{char}", str_obj)

    return str_obj


def translate_schema(singer_schema):
    """ translate a singer schema to a redshift schema """

    # singer types
    sbool = {"type": "boolean"}
    sstring = {"type": "string"}
    snumber = {"type": "number"}
    sinteger = {"type": "integer"}
    sdatetime = {"type": "string", "format": "date-time"}

    def stor(stype):
        """ singer type to redshift type """
        rtype = ""
        if stype == sbool:
            rtype = "BOOLEAN"
        elif stype == sinteger:
            rtype = "INT8"
        elif stype == snumber:
            rtype = "FLOAT8"
        elif stype == sstring:
            rtype = "VARCHAR(256)"
        elif stype == sdatetime:
            rtype = "TIMESTAMP"
        else:
            print((f"WARN: Ignoring type {stype}, "
                   f"it's not supported by the target (yet)."))
        return rtype

    return {escape(f): stor(st) for f, st in singer_schema.items() if stor(st)}


def translate_record(schema, record):
    """ translates a singer record to a redshift record """

    new_record = {}
    for user_field, user_value in record.items():
        new_field = escape(user_field)
        new_value = ""
        if new_field not in schema:
            print((f"WARN: Ignoring field {new_field}, "
                   f"it's not in the streamed schema."))
        elif user_value is not None:
            new_field_type = schema[new_field]
            if new_field_type == "BOOLEAN":
                new_value = f"{escape(user_value).lower()}"
            elif new_field_type == "INT8":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "FLOAT8":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "VARCHAR(256)":
                new_value = f"{user_value}"[0:256]
                while str_len(escape(new_value)) > 256:
                    new_value = new_value[0:-1]
                new_value = f"'{escape(new_value)}'"
            elif new_field_type == "TIMESTAMP":
                new_value = f"'{escape(user_value)}'"
            else:
                print((f"WARN: Ignoring type {new_field_type}, "
                       f"it's not in the streamed schema."))

            new_record[new_field] = new_value
    return new_record


def drop_schema(batcher, schema_name):
    """ drops the schema unless it doesn't exist """
    try:
        batcher.ex(f"DROP SCHEMA \"{schema_name}\" CASCADE", True)
    except postgres.ProgrammingError:
        pass


def drop_table(batcher, schema_name, table_name):
    """ drops the table unless it doesn't exist """
    try:
        statement = f"DROP TABLE \"{schema_name}\".\"{table_name}\" CASCADE"
        batcher.ex(statement, True)
    except postgres.ProgrammingError:
        pass


def create_schema(batcher, schema_name):
    """ creates the schema unless it currently exist """
    try:
        batcher.ex(f"CREATE SCHEMA \"{schema_name}\"", True)
    except postgres.ProgrammingError:
        pass


# pylint: disable=too-many-arguments
def create_table(
        batcher,
        schema_name, table_name,
        table_fields, table_types, table_pkeys):
    """ creates a table on the schema unless it currently exists """
    path = f"\"{schema_name}\".\"{table_name}\""
    fields = ",".join([f"\"{n}\" {table_types[n]}" for n in table_fields])

    try:
        if table_pkeys:
            pkeys = ",".join([f"\"{n}\"" for n in table_pkeys])
            batcher.ex(f"CREATE TABLE {path} ({fields},PRIMARY KEY({pkeys}))")
        else:
            batcher.ex(f"CREATE TABLE {path} ({fields})")
    except postgres.ProgrammingError:
        pass


def rename_schema(batcher, from_name, to_name):
    """ renames the schema unless
            - from_name doesn't exist
            - to_name schema already exists """
    try:
        statement = f"ALTER SCHEMA \"{from_name}\" RENAME TO \"{to_name}\""
        batcher.ex(statement, True)
    except postgres.ProgrammingError:
        pass


# pylint: disable=too-many-instance-attributes
class Batcher():
    """A worker to grab requests from the same table and batch them to Redshift
    """
    def __init__(self, dbcon, dbcur, schema_name):
        print(f"INFO: worker up at {datetime.utcnow()}.")

        self.initt = time.time()

        self.dbcon = dbcon
        self.dbcur = dbcur

        self.sname = schema_name
        self.buckets = {}

    def ex(self, statement, do_print=False):
        """ executes a single statement """
        if do_print:
            print(f"EXEC: {statement}.")
        self.dbcur.execute(statement)

    def queue(self, table_name, values):
        """ queue rows before pushing them in batch to Redshift """
        if table_name not in self.buckets:
            self.buckets[table_name] = {
                "values": [],
                "count": 0,
                "size": 0
            }

        statement = stringify(values, do_group=False)
        stmt_size = str_len(statement)

        # a redshift statement must be less than 16MB, 1KB for the header
        if self.buckets[table_name]["size"] + stmt_size >= 15999000:
            self.load(table_name)

        self.buckets[table_name]["values"].append(statement)
        self.buckets[table_name]["count"] += 1
        self.buckets[table_name]["size"] += stmt_size

    def load(self, table_name, do_print=False):
        """ loads a batch """

        # take every comma separated string, and surround it with parenthesis
        values = stringify(self.buckets[table_name]["values"], do_group=True)

        statement = f"""
            INSERT INTO \"{self.sname}\".\"{table_name}\"
            VALUES {values}"""
        self.ex(statement, do_print)

        count = self.buckets[table_name]["count"]
        size = round(self.buckets[table_name]["size"] / 1.0e6, 2)
        print((f"INFO: {count} rows ({size} MB)"
               f"loaded to Redshift/{self.sname}/{table_name}."))

        self.buckets[table_name]["values"] = []
        self.buckets[table_name]["count"] = 0
        self.buckets[table_name]["size"] = 0

    def flush(self, do_print=False):
        """ flush it at the end to push pending buckets """
        for table_name in self.buckets:
            self.load(table_name, do_print)

    def __del__(self, *args):
        print(f"INFO: worker down at {datetime.utcnow()}.")
        print(f"INFO: {time.time() - self.initt} seconds elapsed.")


# pylint: disable=too-many-locals
def persist_messages(batcher, schema_name, messages):
    """ persist messages received in stdin to Amazon Redshift """
    schema = {}
    ofields = {}
    validator = {}

    for message in messages:
        json_obj = json.loads(message)
        message_type = json_obj["type"]
        if message_type == "RECORD":
            table_name = escape(json_obj["stream"].lower())
            table_schema = schema[table_name]
            table_ofields = ofields[table_name]

            json_record = json_obj["record"]

            try:
                validator[table_name].validate(json_record)
            except jsonschema.exceptions.ValidationError as err:
                print(f"WARN: record did not conform to schema")
                print(err)

            record = translate_record(table_schema, json_record)

            record_ov = []
            for field in table_ofields:
                try:
                    record_ov.append(record[field])
                except KeyError:
                    record_ov.append("null")

            batcher.queue(table_name, record_ov)

        elif message_type == "SCHEMA":
            tname = escape(json_obj["stream"].lower())
            tkeys = tuple(map(escape, json_obj["key_properties"]))
            tschema = json_obj["schema"]

            validator[tname] = jsonschema.Draft4Validator(tschema)

            try:
                validator[tname].check_schema(tschema)
            except jsonschema.exceptions.SchemaError as err:
                print(f"ERROR: schema did not conform to draft 4")
                print(err)
                exit(1)

            schema[tname] = ttypes = translate_schema(tschema["properties"])
            ofields[tname] = tfields = tuple(ttypes.keys())

            create_table(batcher, schema_name, tname, tfields, ttypes, tkeys)

    batcher.flush()


def main():
    """ usual entry point """

    print("\n  Singer target for Amazon Redshift\n")
    print("Fluid Attacks, We hack your software.")
    print("      https://fluidattacks.com/\n")

    # user interface
    parser = argparse.ArgumentParser(
        description="""
            Persists a singer formatted stream to Amazon Redsfhit

            Use:
                tap-anysingertap | target-redshift [params]
        """)
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
    parser.add_argument(
        "-dt", "--drop-tables",
        required=False,
        help="Flag to specify that you want to delete the table if exist",
        action="store_true",
        dest="drop_tables",
        default=False)

    args = parser.parse_args()
    auth = json.load(args.auth)

    target_schema = f"{args.schema_name}"
    backup_schema = f"{target_schema}_backup"
    loading_schema = f"{target_schema}_loading"

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

    # pylint: disable=broad-except
    try:
        (dbcon, dbcur) = make_access_point(auth)

        if args.drop_schema:
            # It means user wants to guarantee 100% data integrity
            # It also implies the use of a loading strategy
            #   to guarantee continuated service availability

            batcher = Batcher(dbcon, dbcur, loading_schema)

            # The loading strategy is:
            #   DROP loading_schema
            drop_schema(batcher, loading_schema)
            #   MAKE loading_schema
            create_schema(batcher, loading_schema)
            #   LOAD loading_schema
            persist_messages(batcher, loading_schema, input_messages)
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
            batcher = Batcher(dbcon, dbcur, target_schema)
            persist_messages(batcher, target_schema, input_messages)
    finally:
        drop_access_point(dbcon, dbcur)


if __name__ == "__main__":
    main()
