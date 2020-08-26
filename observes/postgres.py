"""Manage your postgres database from python.
"""

import json
import argparse

import psycopg2

# ==== little postgres manual
# Returns info
#   SELECT * FROM PG_TABLE_DEF
# Returns tables
#   SELECT * FROM pg_catalog.pg_tables
#   SELECT * FROM pg_catalog.pg_tables WHERE schemaname = "name"
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
    """Returns a cursor to the database.

    Allowed to read and write.
    with the same privileges as the provided profile.

    See: http://initd.org/psycopg/docs/connection.html
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


def main():
    """Usual entry point.
    """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth",
        required=True,
        dest="auth",
        help="JSON authentication file",
        type=argparse.FileType("r"))
    parser.add_argument(
        "-e", "--exec",
        required=True,
        dest="exec",
        help="Command to execute")
    parser.add_argument(
        "-f", "--fetch",
        dest="fetch",
        action="store_true",
        default=False)
    args = parser.parse_args()

    # authentication file
    auth = json.load(args.auth)

    # pylint: disable=broad-except
    try:
        (db_connection, db_cursor) = get_access_point(auth)

        print(f"INFO: Statement to run:\n\"{args.exec}\"\n")
        db_cursor.execute(args.exec)
        print("INFO: Statement ran successfully.\n")

        if args.fetch:
            # prints to console the results of the query
            # it"s used mainly to fetch a SELECT query

            print(f"INFO: Fetching results:\n")
            response_list = db_cursor.fetchall()

            # one row per line, columns between bars
            print("\n".join(
                list(
                    map(
                        lambda row: "|".join(
                            list(
                                map(str, row))), response_list))))

    except (psycopg2.Warning, psycopg2.Error) as exception:
        print(f"INFO: Statement ran with errors:\n{exception}")
    finally:
        close_access_point(db_connection, db_cursor)


if __name__ == "__main__":
    main()
