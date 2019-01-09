"""
Manage your posgres database from python
"""

import json
import argparse

# pylint: disable=import-error
import psycopg2

# ==== little postgres manual
# Returns info
#   SELECT * FROM PG_TABLE_DEF
# Returns tables
#   SELECT * FROM pg_catalog.pg_tables
#   SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'name'
# Push data
#   CREATE SCHEMA newschema AUTHORIZATION user
#   CREATE TABLE newschema.newtable (id int)
#   INSERT INTO newschema.newtable VALUES(123)
# Redshift data types
#   https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html
# Remove data
#   DROP SCHEMA newschema CASCADE
#   DROP TABLE newschema.newtable
# Rename schema
#   ALTER SCHEMA newschema RENAME TO oldschema

def get_access_point(auth):
    """
    returns a cursor to the database
    - allowed to read and write
    - with the same privileges as the provided profile

    see: http://initd.org/psycopg/docs/connection.html
         http://initd.org/psycopg/docs/cursor.html
    """
    db_connection = psycopg2.connect(
        dbname=auth["dbname"],
        user=auth["user"],
        password=auth["password"],
        host=auth["host"],
        port=auth["port"]
    )

    db_connection.set_session(readonly=False)
    db_connection.set_isolation_level(0)

    db_cursor = db_connection.cursor()

    return (db_connection, db_cursor)

def close_access_point(db_connection, db_cursor):
    """ safely close the access points """
    db_cursor.close()
    db_connection.close()

def arguments_error(parser):
    """ Print help and exit """
    parser.print_help()
    exit(1)

def main():
    """ usual entry point """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-auth',
        help='JSON authentication file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-exec',
        help='Command to execute')
    parser.add_argument(
        '--fetch',
        dest='fetch',
        action='store_true')
    args = parser.parse_args()

    if not args.auth:
        arguments_error(parser)

    auth = json.load(args.auth)

    (db_connection, db_cursor) = get_access_point(auth)

    print(f"INFO: Statement to run:\n\"{args.exec}\"\n")

    # pylint: disable=broad-except
    try:
        db_cursor.execute(args.exec)
        print("INFO: Statement ran successfully.\n")
    except Exception as exception:
        print(f"INFO: Statement ran with errors:\n{exception}")
        exit(1)

    if args.fetch:
        print(f"INFO: Fetching results:\n")

        response_list = db_cursor.fetchall()

        # feeling functional
        print("\n".join(list(map(lambda row: "|".join(list(map(str, row))), response_list))))

    close_access_point(db_connection, db_cursor)

if __name__ == "__main__":
    main()
