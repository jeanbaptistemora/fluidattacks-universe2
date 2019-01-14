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

    if not isinstance(str_obj, str):
        str_obj = str(str_obj)

    str_obj = re.sub("\x00", "", str_obj)

    for char in "'\"":
        str_obj = re.sub(char, f"\\{char}", str_obj)

    return str_obj

def translate_schema(singer_schema):
    """ translate a singer schema to a redshift schema """

    # singer types
    sbool = {"type": "boolean"}
    sstring = {"type": "string"}
    snumber = {"type": "number"}
    sdatetime = {"type": "string", "format": "date-time"}

    def stor(stype):
        """ singer type to redshift type """
        rtype = ""
        if stype == sbool:
            rtype = "BOOLEAN"
        elif stype == snumber:
            rtype = "FLOAT8"
        elif stype == sstring:
            rtype = "VARCHAR(1024)"
        elif stype == sdatetime:
            rtype = "TIMESTAMP"
        else:
            print(f"WARN: Ignoring type {stype}, it's not supported by the target (yet).")
        return rtype

    return {escape(f): stor(st) for f, st in singer_schema.items() if stor(st)}

def translate_record(schema, record):
    """ translates a singer record to a redshift record """
    def str_len(str_obj):
        """ returns the number of bytes on a python string """
        return len(str_obj.encode('utf-8'))

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
            elif new_field_type == "FLOAT8":
                new_value = f"{escape(user_value)}"
            elif new_field_type == "VARCHAR(1024)":
                new_value = f"{escape(user_value)}"
                while str_len(new_value) > 1024:
                    new_value = new_value[0:-1]
            elif new_field_type == "TIMESTAMP":
                new_value = f"{escape(user_value)}"
            else:
                print(f"WARN: Ignoring type {new_field_type}, it's not in the streamed schema.")

        new_record[new_field] = new_value
    return new_record

def drop_schema(batcher, schema_name):
    """ drops the schema unless it doesn't exist """
    try:
        batcher.ex(f"DROP SCHEMA \"{schema_name}\" CASCADE")
    except postgres.ProgrammingError:
        pass

def drop_table(batcher, schema_name, table_name):
    """ drops the table unless it doesn't exist """
    try:
        batcher.ex(f"DROP TABLE \"{schema_name}\".\"{table_name}\" CASCADE")
    except postgres.ProgrammingError:
        pass

def create_schema(batcher, schema_name):
    """ creates the schema unless it currently exist """
    try:
        batcher.ex(f"CREATE SCHEMA \"{schema_name}\"")
    except postgres.ProgrammingError:
        pass

# pylint: disable=too-many-arguments
def create_table(batcher, schema_name, table_name, table_fields, table_types, table_pkeys):
    """ creates a table on the schema with (field type) and primary keys """
    path = f"\"{schema_name}\".\"{table_name}\""
    fields = ",".join([f"\"{n}\" {table_types[n]}" for n in table_fields])

    if table_pkeys:
        pkeys = ",".join([f"\"{n}\"" for n in table_pkeys])
        batcher.ex(f"CREATE TABLE {path} ({fields},PRIMARY KEY({pkeys}))")
    else:
        batcher.ex(f"CREATE TABLE {path} ({fields})")

# pylint: disable=too-many-instance-attributes
class Batcher():
    """ A worker to grab requests from the same table and batch them to Redshift """
    def __init__(self, dbcon, dbcur, schema_name):
        print(f"INFO: worker up at {datetime.utcnow()}.")

        self.initt = time.time()

        self.print = False
        self.dbcon = dbcon
        self.dbcur = dbcur

        self.sname = schema_name
        self.tname = "__START"

        self.params = []
        self.template = ""

        self.count = 0

    def ex(self, statement):
        """ executes a single statement, no performance buff here """
        if self.print:
            print(f"EXEC:{statement}.")
        self.dbcur.execute(statement)

    def load(self, table_name, values):
        """ executes multiple statements, big performance buff here """
        self.count += 1
        if self.tname == table_name and self.count < 10000:
            self.params.append(tuple(values))
        else:
            if self.template:
                if self.print:
                    print(f"EXEC:{self.template}.")
                    print(f"EXEC:{self.params}.")
                # dev: need for speed ? try
                # dev: self.dbcur.execute("PREPARE stmt AS complex_query with $1 $2 params")
                execute_values(self.dbcur, self.template, self.params)
                print(f"INFO: {self.count} messages sent to Redshift/{self.sname}/{self.tname}.")
                # dev: self.dbcur.execute("DEALLOCATE stmt")

            # prepare the params list for this batch
            self.count = 0
            self.tname = table_name
            self.params = [tuple(values)]
            self.template = f"INSERT INTO \"{self.sname}\".\"{self.tname}\" VALUES %s"

    def __del__(self, *args):
        print(f"INFO: worker down at {datetime.utcnow()}.")
        print(f"INFO: {time.time() - self.initt} seconds elapsed.")

# pylint: disable=too-many-locals
def persist_messages(dbcon, dbcur, messages, args):
    """ persist messages received in stdin to Amazon Redshift """
    schema = {}
    ofields = {}

    batcher = Batcher(dbcon, dbcur, args.schema_name)

    if args.drop_schema:
        drop_schema(batcher, args.schema_name)

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
                if field in table_record:
                    record_ov.append(table_record[field])
                else:
                    record_ov.append(None)

            batcher.load(table_name, record_ov)

        elif message_type == "SCHEMA":
            table_name = escape(json_obj["stream"].lower())
            table_pkeys = list(map(escape, json_obj["key_properties"]))
            table_schema = json_obj["schema"]

            if args.drop_tables:
                drop_table(batcher, args.schema_name, table_name)

            schema[table_name] = table_ft = translate_schema(table_schema["properties"])
            ofields[table_name] = table_of = list(table_ft.keys())

            create_schema(batcher, args.schema_name)
            create_table(batcher, args.schema_name, table_name, table_of, table_ft, table_pkeys)

    batcher.load("finish", [])

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

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

    # pylint: disable=broad-except
    try:
        (dbcon, dbcur) = make_access_point(auth)
        persist_messages(dbcon, dbcur, input_messages, args)
    finally:
        drop_access_point(dbcon, dbcur)

if __name__ == "__main__":
    main()
