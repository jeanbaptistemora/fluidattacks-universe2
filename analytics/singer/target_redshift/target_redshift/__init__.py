"""
Singer.io target for Amazon Redshift
"""

import io
import re
import sys
import json
import argparse

# pylint: disable=import-error
import psycopg2 as postgres
import psycopg2.extensions as postgres_ext

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
    dbcon.set_isolation_level(postgres_ext.ISOLATION_LEVEL_AUTOCOMMIT)

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
            print(f"WARN: Ignoring type {stype}")
            print(f"REAS: because it's not supported by the target")
        return rtype

    redshift_schema = {escape(f): stor(st) for f, st in singer_schema.items() if stor(st)}
    return redshift_schema

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
            print(f"WARN: Ignoring field {new_field}")
            print(f"REAS: because it's not in the SCHEMA")
        else:
            if schema[new_field] == "BOOLEAN":
                new_value = f"{escape(user_value).lower()}"
            elif schema[new_field] == "FLOAT8":
                new_value = f"{escape(user_value)}"
            elif schema[new_field] == "VARCHAR(1024)":
                new_value = f"'{escape(user_value)}'"
                while str_len(new_value) > 1024:
                    new_value = new_value[0:-2] + new_value[-1]
            elif schema[new_field] == "TIMESTAMP":
                new_value = f"'{escape(user_value)}'"
            else:
                print(f"WARN: Ignoring type {schema[new_field]}")
                print(f"REAS: because it's not supported by the target")

        new_record[new_field] = new_value
    return new_record

def ex(dbcur, statement, print_statement=False):
    """ executes a statement """
    if print_statement:
        print(f"EXEC:{statement}")
    dbcur.execute(statement)

def drop_schema(dbcur, schema_name):
    """ drops the schema unless it doesn't exist """
    try:
        # https://docs.aws.amazon.com/redshift/latest/dg/r_DROP_SCHEMA.html
        ex(dbcur, f"DROP SCHEMA \"{schema_name}\" CASCADE")
    except postgres.ProgrammingError:
        pass

def drop_table(dbcur, schema_name, table_name):
    """ drops the table unless it doesn't exist """
    try:
        # https://docs.aws.amazon.com/redshift/latest/dg/r_DROP_TABLE.html
        ex(dbcur, f"DROP TABLE \"{schema_name}\".\"{table_name}\" CASCADE")
    except postgres.ProgrammingError:
        pass

def create_schema(dbcur, schema_name):
    """ creates the schema unless it currently exist """
    try:
        # https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_SCHEMA.html
        ex(dbcur, f"CREATE SCHEMA \"{schema_name}\"")
    except postgres.ProgrammingError:
        pass

def create_table(dbcur, schema_name, table_name, fields, pkeys):
    """ creates a table on the schema with (field type) and primary keys """
    # https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html
    ex(dbcur, f"CREATE TABLE \"{schema_name}\".\"{table_name}\" ({fields},PRIMARY KEY({pkeys}))")

# pylint: disable=too-many-locals
def persist_messages(dbcon, dbcur, messages, args):
    """ persist messages received in stdin to Amazon Redshift """
    schema = {}

    schema_name = args.schema_name
    do_drop_schema = args.drop_schema
    do_drop_tables = args.drop_tables

    print(f"INFO: receiving messages")

    count_messages = 0
    for message in messages:
        count_messages += 1
        if count_messages % 1000 == 0:
            print(f"INFO: {count_messages} messages sent to Amazon Redshift")

        json_obj = json.loads(message)
        message_type = json_obj["type"]
        if message_type == "RECORD":
            table_name = escape(json_obj["stream"].lower())
            table_schema = schema[table_name]

            try:
                table_record = translate_record(table_schema, json_obj["record"])
            except ValueError as err:
                print(err)
                print(table_name)
                print(table_schema)
                exit()

            fields_values = [(f, v) for f, v in table_record.items() if v]
            fields = ",".join([f"\"{f}\"" for f, v in fields_values])
            values = ",".join([v for f, v in fields_values])

            # https://docs.aws.amazon.com/redshift/latest/dg/r_INSERT_30.html
            ex(dbcur, f"INSERT INTO \"{schema_name}\".\"{table_name}\" ({fields}) VALUES({values})")

        elif message_type == "SCHEMA":
            table_name = escape(json_obj["stream"].lower())
            table_pkeys = list(map(escape, json_obj["key_properties"]))
            table_schema = json_obj["schema"]

            if do_drop_schema:
                drop_schema(dbcur, schema_name)
            elif do_drop_tables:
                drop_table(dbcur, schema_name, table_name)

            schema[table_name] = translate_schema(table_schema["properties"])

            pkeys = ",".join([f"\"{n}\"" for n in table_pkeys])
            fields = ",".join([f"\"{n}\" {t}" for n, t in schema[table_name].items()])

            create_schema(dbcur, schema_name)
            create_table(dbcur, schema_name, table_name, fields, pkeys)

    dbcon.commit()
    print(f"INFO: messages sent successfully")

def main():
    """ usual entry point """

    print("\n  Singer target for Amazon Redshift\n")
    print("Fluid Attacks, We hack your software.")
    print("    https://fluidattacks.com/\n")

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

    print(f"INFO: Pushing all tables to schema \"{args.schema_name}\"\n")

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

    # pylint: disable=broad-except
    try:
        (dbcon, dbcur) = make_access_point(auth)
        persist_messages(dbcon, dbcur, input_messages, args)
    except Exception as exception:
        print(f"Error: {exception}")
    finally:
        drop_access_point(dbcon, dbcur)

if __name__ == "__main__":
    main()
