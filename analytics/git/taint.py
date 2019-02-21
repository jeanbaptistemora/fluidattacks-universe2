#!/usr/bin/env python3
"""Stateless module to manage an stateful database of tainted files."""

import os
import sys
import json
import subprocess
import contextlib

from typing import Iterator, Dict, List, Tuple, Any

import psycopg2 as redshift


# Type aliases that improve clarity
HASH = str
PATH = str
JSON = Any
CONN = Any
CURR = Any


def print_tutorial() -> None:
    """Print help."""
    tutorial: str = """
        Mode of use:
            $ taint.py [command] [args]

        Set data:
            $ taint.py set subscription [subs_name]
                Set the working subscription name.
            $ taint.py set tainted [repo_name] [file_path]
                Mark a file as tainted.
            $ taint.py set clean [repo_name] [file_path]
                Mark a file as clean.

        Get data:
            $ taint.py get subscription
                Return the working subscription name.
            $ taint.py get tainted
                Print all tainted files.
            $ taint.py get clean
                Print all clean files.
            $ taint.py get coverage
                Compute the coverage.

        Admins only:
            $ taint.py init database
                Initialize the database.
            $ taint.py push [repo_path]
                Push the latest data to the database.
        """
    print(tutorial, sep="\n")
    exit(1)


def get_stdout(command: List[str]) -> str:
    """Return the stdout of a command. It's always utf-8 safe."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    raw_stdout, _ = process.communicate()
    stdout = "" if raw_stdout is None else raw_stdout.decode(
        "utf-8", "backslashreplace")
    return stdout


@contextlib.contextmanager
def database(credentials: JSON) -> Iterator[Tuple[CONN, CURR]]:
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
            yield (conn, curr)
        finally:
            curr.close()
    finally:
        conn.close()


def init_database() -> None:
    """Initialize the database."""
    credentials: JSON = get_credentials()

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
                        subs_name      VARCHAR(4096) NOT NULL,
                        repo_name      VARCHAR(4096) NOT NULL,
                        file_path      VARCHAR(4096) NOT NULL,
                        file_state     VARCHAR(8)    NOT NULL,
                        file_last_hash VARCHAR(40)   NOT NULL,
                        PRIMARY KEY(
                            subs_name,
                            repo_name,
                            file_path
                        )
                    )
                """)
            conn.commit()
        except redshift.ProgrammingError:
            print("ERRR: Does table taints.data currently exist?")


def push_repo(repo_path: str) -> None:
    """Push the latest data to the database."""
    credentials: JSON = get_credentials()

    subs_name: str = get_subs_name()
    repo_name = os.path.basename(repo_path)

    local_file_states = push_repo__get_local_files_states(
        repo_path)
    remote_file_states = push_repo__get_remote_file_states(
        credentials, subs_name, repo_name)

    for file_path in local_file_states:
        file_last_hash = local_file_states[file_path]["file_last_hash"]
        if file_path in remote_file_states:
            remote_file_last_hash = \
                remote_file_states[file_path]["file_last_hash"]
            if not file_last_hash == remote_file_last_hash:
                # a commit has changed the file, update it in remote as tainted
                row_upsert(
                    credentials,
                    subs_name,
                    repo_name,
                    file_path,
                    "tainted",
                    file_last_hash)
        else:
            # a new file is in HEAD, push it to remote as tainted
            row_insert(
                credentials,
                subs_name,
                repo_name,
                file_path,
                "tainted",
                file_last_hash)

    for file_path in remote_file_states:
        if file_path not in local_file_states:
            # remote contains a file that is not in HEAD now, delete it
            row_delete(
                credentials,
                subs_name,
                repo_name,
                file_path)


def push_repo__get_file_last_hash(
        repo_path: str,
        file_path: str) -> HASH:
    """Return the last commit hash that modified a file."""
    command: List[str] = [
        "git", "-C", repo_path,
        "log", "--format=%H", "--max-count", "1", "--", file_path]
    file_last_hash = get_stdout(command)[0:-1]
    return file_last_hash


def push_repo__get_local_files_states(
        repo_path: str) -> Dict[str, Dict[str, str]]:
    """Return a mapping of file states in local HEAD."""
    command: List[str] = \
        ["git", "-C", repo_path, "ls-tree", "--name-only", "-r", "HEAD"]
    local_files_in_head: List[PATH] = \
        get_stdout(command)[0:-1].splitlines()
    local_file_states: Dict[str, Dict[str, str]] = {
        file_path: {
            "file_state": "not set",
            "file_last_hash": push_repo__get_file_last_hash(
                repo_path, file_path)
        }
        for file_path in local_files_in_head
    }
    return local_file_states


def push_repo__get_remote_file_states(
        credentials: JSON,
        subs_name: str,
        repo_name: str) -> Dict[str, Dict[str, str]]:
    """Return a mapping of file states in remote HEAD."""
    with database(credentials) as (conn, curr):
        curr.execute(f"""
            SELECT
                file_path,
                file_state,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = '{subs_name}' and
                repo_name = '{repo_name}'
            """)
        conn.commit()
        remote_file_states: Dict[str, Dict[str, str]] = {
            file_path: {
                "file_last_hash": file_last_hash,
                "file_state": file_state
            }
            for file_path, file_state, file_last_hash in curr
        }
        return remote_file_states


def row_insert(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str,
        file_state: str,
        file_last_hash: HASH) -> None:
    """Insert a row into the database."""
    # pylint: disable=too-many-arguments
    with database(credentials) as (conn, curr):
        curr.execute(f"""
            INSERT INTO
                taints.data (
                    subs_name,
                    repo_name,
                    file_path,
                    file_state,
                    file_last_hash
                )
            VALUES (
                '{subs_name}',
                '{repo_name}',
                '{file_path}',
                '{file_state}',
                '{file_last_hash}'
            )
            """)
        conn.commit()


def row_delete(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str) -> None:
    """Delete a row into the database."""
    with database(credentials) as (conn, curr):
        curr.execute(f"""
            DELETE FROM
                taints.data
            WHERE
                subs_name = '{subs_name}' and
                repo_name = '{repo_name}' and
                file_path = '{file_path}'
            """)
        conn.commit()


def row_upsert(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str,
        file_state: str,
        file_last_hash: HASH) -> None:
    """Upsert a row into the database."""
    # pylint: disable=too-many-arguments
    row_delete(
        credentials,
        subs_name,
        repo_name,
        file_path)
    row_insert(
        credentials,
        subs_name,
        repo_name,
        file_path,
        file_state,
        file_last_hash)


def row_get_by_index(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str) -> Tuple[Any, Any]:
    """Get file_state, file_last_hash from row."""
    with database(credentials) as (conn, curr):
        curr.execute(f"""
            SELECT
                file_state,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = '{subs_name}' and
                repo_name = '{repo_name}' and
                file_path = '{file_path}'
            """)
        conn.commit()
        for row in curr:
            file_state, file_last_hash = row
            break
        else:
            file_state, file_last_hash = None, None
        return file_state, file_last_hash


def row_get_all_with_state(
        credentials: JSON,
        subs_name: str,
        file_state: str) -> Iterator[Tuple[str, str, str]]:
    """Yield repo_name, file_path, file_last_hash that matches file_state."""
    with database(credentials) as (conn, curr):
        curr.execute(f"""
            SELECT
                repo_name,
                file_path,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = '{subs_name}' and
                file_state = '{file_state}'
            ORDER BY
                subs_name,
                file_path
            """)
        conn.commit()
        for repo_name, file_path, file_last_hash in curr:
            yield repo_name, file_path, file_last_hash


def get_credentials() -> JSON:
    """Return a JSON with the credentials read from vault."""
    vault_credentials_stdout: str = get_stdout(
        ["vault", "read", "-field=analytics_auth_redshift", "secret/serves"])
    try:
        credentials: JSON = json.loads(vault_credentials_stdout)
    except json.decoder.JSONDecodeError:
        print("WARN: Are you logged in vault?")
        exit(1)
    return credentials


def get_subs_name(do_print=False) -> str:
    """Return the working subscription name."""
    state_file_path = f"{os.path.dirname(__file__)}/.state"
    if os.path.isfile(state_file_path):
        with open(state_file_path, "r") as state_file:
            subs_name: str = state_file.read()
    else:
        print("WARN: You must set the subscription name first.")
        exit(1)
    if do_print:
        print(f"INFO: Working on {subs_name}.")
    return subs_name


def get_files_with_state(file_state: str) -> None:
    """Print all files with file_state."""
    credentials: JSON = get_credentials()
    subs_name: str = get_subs_name()

    print(f"INFO: For subscription {subs_name}, files marked as {file_state}:")
    for repo_name, file_path, file_last_hash in \
            row_get_all_with_state(credentials, subs_name, file_state):
        print(f"{repo_name}/{file_path} [{file_last_hash}]")


def set_subs_name(subs_name: str) -> None:
    """Set the working subscription name."""
    state_file_path = f"{os.path.dirname(__file__)}/.state"
    with open(state_file_path, "w") as state_file:
        state_file.write(subs_name)
        print("INFO: subscription name set.")


def set_file_state(
        repo_name: str,
        file_path: str,
        file_state_new: str) -> None:
    """Mark a file as tainted."""
    credentials: JSON = get_credentials()
    subs_name: str = get_subs_name()

    print(f"Attemting to mark as {file_state_new}:")
    print(f"  subs_name:      {subs_name}")
    print(f"  repo_name:      {repo_name}")
    print(f"  file_path:      {file_path}")
    file_state, file_last_hash = \
        row_get_by_index(credentials, subs_name, repo_name, file_path)
    if file_state:
        print(f"  file_state:     {file_state}")
        print(f"  file_last_hash: {file_last_hash}")
        if input("Type 'yes' to confirm: ") == "yes":
            row_upsert(
                credentials,
                subs_name,
                repo_name,
                file_path,
                file_state_new,
                file_last_hash)
            print("\nINFO: Done.")
    else:
        print("WARN: You can not modify non-existing rows.")


def main():
    """Usual entry point."""
    # command line interface
    args = iter(sys.argv[1:])
    cmd = next(args, "")
    arg1 = next(args, "")
    arg2 = next(args, "")
    arg3 = next(args, "")

    # Set data
    if cmd == "set" and arg1 == "subscription":
        subs_name = arg2
        set_subs_name(subs_name)
    elif cmd == "set" and arg1 == "tainted":
        repo_name = arg2
        file_path = arg3
        set_file_state(repo_name, file_path, "tainted")
    elif cmd == "set" and arg1 == "clean":
        repo_name = arg2
        file_path = arg3
        set_file_state(repo_name, file_path, "clean")
    # Get data
    elif cmd == "get" and arg1 == "subscription":
        get_subs_name(do_print=True)
    elif cmd == "get" and arg1 == "tainted":
        get_files_with_state("tainted")
    elif cmd == "get" and arg1 == "clean":
        get_files_with_state("clean")
    elif cmd == "get" and arg1 == "coverage":
        pass
    # Admins only
    elif cmd == "init" and arg1 == "database":
        init_database()
    elif cmd == "push":
        repo_path = os.path.abspath(arg1)
        push_repo(repo_path)
    else:
        print_tutorial()


if __name__ == "__main__":
    main()
