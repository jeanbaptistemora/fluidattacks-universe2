"""
Singer.io target for Amazon Redshift
"""

import io
import re
import sys
import json
import time
import argparse

from datetime import datetime

# pylint: disable=import-error
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions

from psycopg2.extras import execute_values

# identity function
IDM = lambda x: x

# stringifies an iterable
#   it: (a, b, c) => "(f(a)),(f(b)),(f(c))"
STRINGIFY = lambda it, c=",", b="(", e=")", f=IDM: c.join(f"{b}{f(x)}{e}" for x in it)

STR_LEN = lambda str_obj: len(str_obj.encode('utf-8'))

def make_access_point(auth):
    """ returns a connection and a cursor to the database """
    # dev note, http://initd.org/psycopg/docs/extras.html

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

def drop_access_point(dbcon, dbcur):
    """ safely close the access points """
    dbcur.close()
    dbcon.close()

def escape(str_obj):
    """ scape characters """

    str_obj = str(str_obj)
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
            print(f"WARN: Ignoring type {stype}, it's not supported by the target (yet).")
        return rtype

    return {escape(f): stor(st) for f, st in singer_schema.items() if stor(st)}

def translate_record(schema, record):
    """ translates a singer record to a redshift record """

    new_record = {}
    for user_field, user_value in record.items():
        new_field = escape(user_field)
        new_value = ""
        if not new_field in schema:
            print(f"WARN: Ignoring field {new_field}, it's not in the streamed schema.")
        else:
            new_field_type = schema[new_field]
            if new_field_type == "BOOLEAN":
                new_value = f"{escape(user_value).lower()}"
            elif new_field_type == "INT8":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "FLOAT8":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "VARCHAR(256)":
                new_value = user_value[0:256]
                while STR_LEN(escape(new_value)) > 256:
                    new_value = new_value[0:-1]
                new_value = f"'{escape(new_value)}'"
            elif new_field_type == "TIMESTAMP":
                new_value = f"'{escape(user_value)}'"
            else:
                print(f"WARN: Ignoring type {new_field_type}, it's not in the streamed schema.")

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
        batcher.ex(f"DROP TABLE \"{schema_name}\".\"{table_name}\" CASCADE", True)
    except postgres.ProgrammingError:
        pass

def create_schema(batcher, schema_name):
    """ creates the schema unless it currently exist """
    try:
        batcher.ex(f"CREATE SCHEMA \"{schema_name}\"", True)
    except postgres.ProgrammingError:
        pass

# pylint: disable=too-many-arguments
def create_table(batcher, schema_name, table_name, table_fields, table_types, table_pkeys):
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
        batcher.ex(f"ALTER SCHEMA \"{from_name}\" RENAME TO \"{to_name}\"", True)
    except postgres.ProgrammingError:
        pass

# pylint: disable=too-many-instance-attributes
class Batcher():
    """ A worker to grab requests from the same table and batch them to Redshift """
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
        if not table_name in self.buckets:
            self.buckets[table_name] = {
                "values": [],
                "count": 0,
                "size": 0
            }

        statement = STRINGIFY(values, c=",", b="", e="")
        stmt_size = STR_LEN(statement)

        # a redshift statement must be less than 16MB, reserve 1KB for the header
        if self.buckets[table_name]["size"] + stmt_size >= 15999000:
            self.load(table_name)

        self.buckets[table_name]["values"].append(statement)
        self.buckets[table_name]["count"] += 1
        self.buckets[table_name]["size"] += stmt_size

    def load(self, table_name, do_print=False):
        """ loads a batch """

        # take every comma separated string, and surround it with parenthesis
        values = STRINGIFY(self.buckets[table_name]["values"], c=",", b="(", e=")")

        self.ex(f"INSERT INTO \"{self.sname}\".\"{table_name}\" VALUES {values}", do_print)

        count = self.buckets[table_name]["count"]
        size = round(self.buckets[table_name]["size"] / 1.0e6, 2)
        print(f"INFO: {count} rows ({size} MB) loaded to Redshift/{self.sname}/{table_name}.")

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

    for message in messages:
        json_obj = json.loads(message)
        message_type = json_obj["type"]
        if message_type == "RECORD":
            table_name = escape(json_obj["stream"].lower())
            table_schema = schema[table_name]
            table_ofields = ofields[table_name]

            table_record = translate_record(table_schema, json_obj["record"])

            record_ov = []
            for field in table_ofields:
                try:
                    record_ov.append(table_record[field])
                except KeyError:
                    record_ov.append("null")

            batcher.queue(table_name, record_ov)

        elif message_type == "SCHEMA":
            table_name = escape(json_obj["stream"].lower())
            table_pkeys = tuple(map(escape, json_obj["key_properties"]))
            table_schema = json_obj["schema"]

            schema[table_name] = table_ft = translate_schema(table_schema["properties"])
            ofields[table_name] = table_of = tuple(table_ft.keys())

            create_table(batcher, schema_name, table_name, table_of, table_ft, table_pkeys)

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
        help="Pass this flag to specify that you want to delete the schema if exist",
        action="store_true",
        dest="drop_schema",
        default=False)
    parser.add_argument(
        "-dt", "--drop-tables",
        required=False,
        help="Pass this flag to specify that you want to delete a streamed table if exist",
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

        batcher = Batcher(dbcon, dbcur, loading_schema)

        if args.drop_schema:
            # It means user wants to guarantee 100% data integrity
            # It also implies the use of a loading strategy
            #   to guarantee continuated service availability

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
            # It means user only wants to push data and just cares about having it there
            #   the trade-off is:
            #     - data integrity
            #     - possible un-updated schema
            #     - and dangling/orphan/duplicated records
            persist_messages(batcher, target_schema, input_messages)
    finally:
        drop_access_point(dbcon, dbcur)

if __name__ == "__main__":
    main()
