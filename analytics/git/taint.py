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

        Commands and args:
            $ taint.py taint [repo_name:file])
                Taint a file.
            $ taint.py untaint [repo_name:file]
                Untaint a file.
            $ taint.py get tainted
                Print all tainted files in the format [repo_name:file].
            $ taint.py get stats
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

    subs_name: str = get_subs_name()
    credentials: JSON = get_credentials()

    repo_name = os.path.basename(repo_path)

    local_file_states = push_repo__get_local_files_states(
        repo_path)
    remote_file_states = push_repo__get_remote_file_states(
        credentials, subs_name, repo_name)

    # if file in (local but not remote) {push to remote as taint}
    for local_file in local_file_states:
        if local_file in remote_file_states:
            # verify file_last_hash
            pass
        else:
            # push to remote as tainted
            pass
    for remote_file in remote_file_states:
        if remote_file not in local_file_states:
            # delete row
            pass


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
                taints.data.subs_name = '{subs_name}' and
                taints.data.repo_name = '{repo_name}'
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


def get_subs_name() -> str:
    """Return the subscription name."""
    state_file_path = f"{os.path.dirname(__file__)}/.state"
    if os.path.isfile(state_file_path):
        with open(state_file_path, "r") as state_file:
            subs_name: str = state_file.read()
    else:
        print("WARN: You must set the subscription name first.")
        exit(1)
    return subs_name


def set_subs_name(subs_name: str) -> None:
    """Set the subs_name."""
    state_file_path = f"{os.path.dirname(__file__)}/.state"
    with open(state_file_path, "w") as state_file:
        state_file.write(subs_name)
        print("INFO: subscription name set.")


def main():
    """Usual entry point."""
    # command line interface
    cli_arg_list: List[str] = sys.argv
    cli_arg_count: int = len(cli_arg_list)

    # at least two parameters must be supplied
    if cli_arg_count <= 2:
        print_tutorial()

    # parse and dispatch
    cmd = cli_arg_list[1]
    arg = cli_arg_list[2]
    if cmd == "init" and arg == "database":
        init_database()
    elif cmd == "set-subscription":
        subs_name = arg
        set_subs_name(subs_name)
    elif cmd == "push":
        repo_path = os.path.abspath(arg)
        push_repo(repo_path)
    else:
        print_tutorial()


if __name__ == "__main__":
    main()
