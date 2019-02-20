#!/usr/bin/env python3
"""Stateless module to manage an stateful database of tainted files."""

import os
import sys
import json
import contextlib

from typing import Iterator, List, Tuple, Any

import psycopg2 as redshift


# Type aliases that improve clarity
JSON = Any
CONN = Any
CURR = Any


def print_tutorial() -> None:
    """Print help."""
    tutorial: str = """
        Mode of use:
            $ taint.py [command] [args]

        Commands and args:
            $ taint.py stats
                Compute the coverage.
            $ taint.py show-tainted
                Print all tainted files in the format [repository:file].
            $ taint.py untaint [repository:file]
                Untaint a file.
            $ taint.py taint [repository:file])
                Taint a file.

        Admins only:
            $ taint.py init database
                Initialize the database.
            $ taint.py push [repository-path]
                Push the latest data to the database.

        Requires:
            $ export ANALYTICS_TAINT_SUBSCRIPTION="subscription to track".
        """
    print(tutorial, sep="\n")
    exit(1)


@contextlib.contextmanager
def database(credentials) -> Iterator[Tuple[CONN, CURR]]:
    """Context manager to get a safe connection and a cursor."""
    conn = redshift.connect(
        dbname=credentials["dbname"],
        user=credentials["user"],
        password=credentials["password"],
        host=credentials["host"],
        port=credentials["port"])
    try:
        curr = conn.cursor()
        try:
            yield conn, curr
        finally:
            curr.close()
    finally:
        conn.close()


def init_database(credentials) -> None:
    """Initialize the database."""
    with database(credentials) as (conn, curr):
        print("INFO: Creating schema taints.")
        try:
            curr.execute("""
                CREATE SCHEMA
                    taints
                """)
            conn.commit()
        except redshift.ProgrammingError:
            print("ERRR: Does schema taints currently exist?")

    with database(credentials) as (conn, curr):
        print("INFO: Creating table data on schema taints.")
        try:
            curr.execute("""
                CREATE TABLE
                    taints.data (
                        subscription VARCHAR(1024) NOT NULL,
                        repository VARCHAR(1024) NOT NULL,
                        sha1 VARCHAR(1024) NOT NULL,
                        file VARCHAR(1024) NOT NULL,
                        PRIMARY KEY(
                            subscription,
                            repository,
                            sha1,
                            file
                        )
                    )
                """)
            conn.commit()
        except redshift.ProgrammingError:
            print("ERRR: Does table taints.data exist?")


def push_repository(credentials, subscription, repository_path):
    """Push the latest data to the database."""
    return credentials, subscription, repository_path


def get_credentials() -> JSON:
    """Return a JSON with the credentials read from vault."""
    credentials: JSON = json.loads(os.popen((
        "vault read -field=analytics_auth_redshift secret/serves")).read())
    return credentials


def get_subscription() -> str:
    """Return the path to the subscription."""
    subscription: str = os.environ["ANALYTICS_TAINT_SUBSCRIPTION"]
    return subscription


def main():
    """Usual entry point."""
    # command line interface
    cli_arg_list: List[str] = sys.argv
    cli_arg_count: int = len(cli_arg_list)

    # at least two parameters must be supplied
    if cli_arg_count <= 2:
        print_tutorial()

    # parameters
    credentials: JSON = get_credentials()
    subscription: str = get_subscription()

    # parse and dispatch
    cmd = cli_arg_list[1]
    arg = cli_arg_list[2]
    if cmd == "init" and arg == "database":
        init_database(credentials)
    elif cmd == "push":
        repository_path = arg
        push_repository(credentials, subscription, repository_path)
    else:
        print_tutorial()


if __name__ == "__main__":
    main()
