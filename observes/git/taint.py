#!/usr/bin/env python3
"""Stateless module to manage an stateful database of tainted files."""

import os
import re
import csv
import sys
import json
import codecs
import subprocess
import contextlib

from typing import Iterable, Iterator, Dict, List, Tuple, Any

import psycopg2 as redshift

# Type aliases that improve clarity
HASH = str
PATH = str
JSON = Any
CONN = Any
CURR = Any

# constants
EMPTY_TREE_HASH: HASH = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=possibly-unused-variable


def print_tutorial() -> None:
    """Print help."""
    tutorial: str = """
        Mode of use:
            $ taint.py [command] [args]

        Set data:
            $ taint.py set subscription [subs_name]
                Set the working subscription name.
            $ taint.py set username [user_name]
                Set the working user name.
            $ taint.py set tainted [repo_name] [file_path]
                Mark a file as tainted.
            $ taint.py set clean [repo_name] [file_path]
                Mark a file as clean.

        Get data:
            $ taint.py get configurations
                Return the working configurations.
            $ taint.py get tainted
                Print all tainted files.
            $ taint.py get clean
                Print all clean files.
            $ taint.py get coverage
                Compute the coverage for the working subscription.
            $ taint.py get coverages
                Compute the coverage for all groups.

        Admins only:
            $ taint.py database init
                Initialize the database.
            $ taint.py database push [repo_path]
                Push the latest data to the database.
            $ taint.py database wring [lines_csv_path]
                Wring the lines.csv file to extract information from it.
            $ taint.py database remove repository [repo_name]
                Remove a repository from the database.
            $ taint.py database vacuum
                Vacuum tables to improve query performance.
        """
    print(tutorial, sep="\n")
    sys.exit(1)


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


def database_init() -> None:
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
            print("WARN: Does schema taints currently exist?")

    with database(credentials) as (conn, curr):
        print("INFO: Creating table data on schema taints.")
        try:
            curr.execute("""
                CREATE TABLE
                    taints.data (
                        subs_name      VARCHAR(4096) NOT NULL,
                        repo_name      VARCHAR(4096) NOT NULL,
                        file_path      VARCHAR(4096) NOT NULL,
                        file_lines     INT8          NOT NULL,
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
            print("WARN: Does table taints.data currently exist?")

    with database(credentials) as (conn, curr):
        print("INFO: Creating table logs on schema taints.")
        try:
            curr.execute("""
                CREATE TABLE
                    taints.logs (
                        date           TIMESTAMP     NOT NULL,
                        summary        VARCHAR(256)  NOT NULL,
                        user_name      VARCHAR(256)  NOT NULL,
                        subs_name      VARCHAR(4096) NOT NULL,
                        repo_name      VARCHAR(4096) NOT NULL,
                        file_path      VARCHAR(4096) NOT NULL,
                        file_lines     INT8          NOT NULL,
                        file_state     VARCHAR(8)    NOT NULL,
                        file_last_hash VARCHAR(40)   NOT NULL
                    )
                """)
            conn.commit()
        except redshift.ProgrammingError:
            print("WARN: Does table taints.logs currently exist?")


def database_remove_repository(repo_name: str) -> None:
    """Remove a repository from the database."""
    credentials: JSON = get_credentials()

    summary: str = 'deleted'
    subs_name: str = get_subs_name()
    user_name: str = get_user_name()

    print(f"INFO: Do you really want to delete {repo_name} from the database?")
    if not input("Type 'yes' to confirm: ") == "yes":
        print("INFO: Aborted.")
        return

    with database(credentials) as (conn, curr):
        curr.execute("""
            INSERT INTO
                taints.logs (
                    date,
                    summary,
                    user_name,
                    subs_name,
                    repo_name,
                    file_path,
                    file_lines,
                    file_state,
                    file_last_hash
                )
            SELECT
                GETDATE(),
                %(summary)s,
                %(user_name)s,
                subs_name,
                repo_name,
                file_path,
                file_lines,
                file_state,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = %(subs_name)s and
                repo_name = %(repo_name)s
            """, dict(locals().items()))
        conn.commit()

    with database(credentials) as (conn, curr):
        curr.execute("""
            DELETE FROM
                taints.data
            WHERE
                subs_name = %(subs_name)s and
                repo_name = %(repo_name)s
            """, dict(locals().items()))
        conn.commit()

    print("INFO: Done.")


def database_vacuum() -> None:
    """Vacuum tables to improve query performance."""
    credentials: JSON = get_credentials()

    for table in ("data", "logs"):
        with database(credentials) as (conn, curr):
            print(f"INFO: Vacuuming {table} data on schema taints.")
            try:
                curr.execute(f"""
                    END TRANSACTION;
                    VACUUM FULL taints.{table} TO 100 PERCENT;
                """)
                conn.commit()
                print("INFO: Done.")
            except (redshift.ProgrammingError, redshift.NotSupportedError):
                print("ERRR: Please try again later.")


def database_push(repo_path: str) -> None:
    """Push the latest data to the database."""
    credentials: JSON = get_credentials()

    subs_name: str = get_subs_name()
    repo_name = os.path.basename(repo_path)

    print(f"INFO: Pushing {repo_path} to the database, please wait.")

    local_file_states = database_push__get_local_files_states(
        repo_path)
    remote_file_states = database_push__get_remote_file_states(
        credentials, subs_name, repo_name)

    for file_path in local_file_states:
        file_lines = local_file_states[file_path]["file_lines"]
        file_last_hash = local_file_states[file_path]["file_last_hash"]
        if file_path in remote_file_states:
            remote_file_last_hash = \
                remote_file_states[file_path]["file_last_hash"]
            if not file_last_hash == remote_file_last_hash:
                # a commit has changed the file, update it in remote as tainted
                row__data__upsert(
                    credentials,
                    subs_name,
                    repo_name,
                    file_path,
                    file_lines,
                    "tainted",
                    file_last_hash)
                row__logs__insert(
                    credentials,
                    "changed",
                    "admin",
                    subs_name,
                    repo_name,
                    file_path,
                    file_lines,
                    "tainted",
                    file_last_hash)
        else:
            # a new file is in HEAD, push it to remote as tainted
            row__data__insert(
                credentials,
                subs_name,
                repo_name,
                file_path,
                file_lines,
                "tainted",
                file_last_hash)
            row__logs__insert(
                credentials,
                "added",
                "admin",
                subs_name,
                repo_name,
                file_path,
                file_lines,
                "tainted",
                file_last_hash)

    for file_path in remote_file_states:
        if file_path not in local_file_states:
            # remote contains a file that is not in HEAD now, delete it
            file_lines = remote_file_states[file_path]["file_lines"]
            file_last_hash = remote_file_states[file_path]["file_last_hash"]
            row__data__delete(
                credentials,
                subs_name,
                repo_name,
                file_path)
            row__logs__insert(
                credentials,
                "removed",
                "admin",
                subs_name,
                repo_name,
                file_path,
                file_lines,
                "clean",
                file_last_hash)

    print("INFO: Done.")


def database_push__get_file_last_hash(
        repo_path: str,
        file_path: str) -> HASH:
    """Return the last commit hash that modified a file."""
    command: List[str] = [
        "git", "-C", repo_path,
        "log", "--format=%H", "--max-count", "1", "--", file_path]
    file_last_hash = get_stdout(command)[0:-1]
    return file_last_hash


def database_push__get_file_lines(
        repo_path: str,
        file_path: str) -> int:
    """Return the number of lines in a file."""
    file_path = codecs.escape_decode(file_path)[0] # type: ignore # noqa
    command: List[str] = [
        "git", "-C", repo_path,
        "diff", "--numstat", EMPTY_TREE_HASH, file_path]
    raw_command_output: str = get_stdout(command)[0:-1]
    # binary files produce "-(tab)-(tab)(file_path)"
    # non-binary files produce "(int)(tab)(int)(tab)(file_path)"
    raw_file_lines: str = raw_command_output.split("\t")[0]
    file_lines: int = int(raw_file_lines) if not raw_file_lines == "-" else 0
    return file_lines


def database_push__get_local_files_states(
        repo_path: str) -> Dict[str, Dict[str, Any]]:
    """Return a mapping of file states in local HEAD."""
    command: List[str] = \
        ["git", "-C", repo_path, "ls-tree", "--name-only", "-r", "HEAD"]
    local_files_in_head: List[PATH] = \
        get_stdout(command)[0:-1].splitlines()

    # when a string is backslash-replaced, python round it with quotes
    # we must remove it by hand
    local_files_in_head = [
        path[1:-1] if path[0] == '"' and path[-1] == '"' else path
        for path in local_files_in_head
    ]

    local_file_states: Dict[str, Dict[str, Any]] = {
        file_path: {
            "file_lines": database_push__get_file_lines(
                repo_path, file_path),
            "file_state": "not set",
            "file_last_hash": database_push__get_file_last_hash(
                repo_path, file_path)
        }
        for file_path in local_files_in_head
    }
    return local_file_states


def database_push__get_remote_file_states(
        credentials: JSON,
        subs_name: str,
        repo_name: str) -> Dict[str, Dict[str, Any]]:
    """Return a mapping of file states in remote HEAD."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            SELECT
                file_path,
                file_lines,
                file_state,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = %(subs_name)s and
                repo_name = %(repo_name)s
            """, dict(locals().items()))
        conn.commit()
        remote_file_states: Dict[str, Dict[str, Any]] = {
            file_path: {
                "file_lines": file_lines,
                "file_state": file_state,
                "file_last_hash": file_last_hash
            }
            for file_path, file_lines, file_state, file_last_hash in curr
        }
        return remote_file_states


def database_wring(lines_csv_path: str) -> None:
    """Wring the lines.csv file to extract information from it."""
    credentials: JSON = get_credentials()

    subs_name: str = get_subs_name()

    print(f"INFO: Extracting information from {lines_csv_path}, please wait.")

    with open(lines_csv_path, "r") as lines_csv:
        reader = csv.DictReader(
            lines_csv,
            fieldnames=[
                "repo_name__file_path",
                "file_lines_a",
                "file_lines_b",
                "-",
                "file_revision_hash"])
        next(reader)
        for row in reader:
            if row["file_lines_a"] == row["file_lines_b"]:
                repo_name, file_path = \
                    row["repo_name__file_path"].split("/", 1)
                file_revision_hash: HASH = row["file_revision_hash"]
                if database_wring__verify_up_to_date(
                        credentials,
                        subs_name,
                        repo_name,
                        file_path,
                        file_revision_hash):
                    set_file_state(
                        repo_name,
                        file_path,
                        "clean",
                        comfirmation=True)

    print("INFO: Done.")


def database_wring__verify_up_to_date(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str,
        file_revision_hash: HASH) -> bool:
    """Verify if this file has been reviewed at his last known state."""
    file_lines, file_state, file_last_hash = \
        row__data__get_by_index(credentials, subs_name, repo_name, file_path)
    if file_lines and file_state == "tainted" and file_revision_hash:
        file_revision_hash = file_revision_hash.lower()
        revision_is_hash = re.match(r"[0-9a-f]{7,40}", file_revision_hash)
        revision_is_last = re.match(f"^{file_revision_hash}", file_last_hash)
        if revision_is_hash and revision_is_last:
            return True
    return False


def row__data__insert(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str,
        file_lines: int,
        file_state: str,
        file_last_hash: HASH) -> None:
    """Insert a row into the database."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            INSERT INTO
                taints.data (
                    subs_name,
                    repo_name,
                    file_path,
                    file_lines,
                    file_state,
                    file_last_hash
                )
            VALUES (
                %(subs_name)s,
                %(repo_name)s,
                %(file_path)s,
                %(file_lines)s,
                %(file_state)s,
                %(file_last_hash)s
            )
            """, dict(locals().items()))
        conn.commit()


def row__data__delete(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str) -> None:
    """Delete a row into the database."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            DELETE FROM
                taints.data
            WHERE
                subs_name = %(subs_name)s and
                repo_name = %(repo_name)s and
                file_path = %(file_path)s
            """, dict(locals().items()))
        conn.commit()


def row__data__upsert(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str,
        file_lines: int,
        file_state: str,
        file_last_hash: HASH) -> None:
    """Upsert a row into the database."""
    row__data__delete(
        credentials,
        subs_name,
        repo_name,
        file_path)
    row__data__insert(
        credentials,
        subs_name,
        repo_name,
        file_path,
        file_lines,
        file_state,
        file_last_hash)


def row__data__get_by_index(
        credentials: JSON,
        subs_name: str,
        repo_name: str,
        file_path: str) -> Tuple[Any, Any, Any]:
    """Get file_state, file_last_hash from row."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            SELECT
                file_lines,
                file_state,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = %(subs_name)s and
                repo_name = %(repo_name)s and
                file_path = %(file_path)s
            """, dict(locals().items()))
        conn.commit()
        for row in curr:
            file_lines, file_state, file_last_hash = row
            break
        else:
            file_lines, file_state, file_last_hash = None, None, None
        return file_lines, file_state, file_last_hash


def row__data__get_all_with_state(
        credentials: JSON,
        subs_name: str,
        file_state: str) -> Iterator[Tuple[str, str, int, str]]:
    """Yield repo_name, file_path, file_last_hash that matches file_state."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            SELECT
                repo_name,
                file_path,
                file_lines,
                file_last_hash
            FROM
                taints.data
            WHERE
                subs_name = %(subs_name)s and
                file_state = %(file_state)s
            ORDER BY
                repo_name,
                file_path,
                file_lines
            """, dict(locals().items()))
        conn.commit()
        for repo_name, file_path, file_lines, file_last_hash in curr:
            yield repo_name, file_path, file_lines, file_last_hash


def row__logs__insert(
        credentials: JSON,
        summary: str,
        user_name: str,
        subs_name: str,
        repo_name: str,
        file_path: str,
        file_lines: int,
        file_state: str,
        file_last_hash: HASH) -> None:
    """Insert a row into the database."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            INSERT INTO
                taints.logs (
                    date,
                    summary,
                    user_name,
                    subs_name,
                    repo_name,
                    file_path,
                    file_lines,
                    file_state,
                    file_last_hash
                )
            VALUES (
                GETDATE(),
                %(summary)s,
                %(user_name)s,
                %(subs_name)s,
                %(repo_name)s,
                %(file_path)s,
                %(file_lines)s,
                %(file_state)s,
                %(file_last_hash)s
            )
            """, dict(locals().items()))
        conn.commit()


def get_all_groups(credentials: JSON) -> List[str]:
    """Return a list with all groups in the database."""
    with database(credentials) as (conn, curr):
        curr.execute("""
            SELECT
                DISTINCT(subs_name)
            FROM
                taints.data
            ORDER BY
                subs_name
            """)
        conn.commit()
        return [row[0] for row in curr]


def get_credentials() -> JSON:
    """Return a JSON with the credentials read from vault."""
    vault_credentials_stdout: str = get_stdout(
        ["vault", "read", "-field=analytics_auth_redshift", "secret/serves"])
    try:
        credentials: JSON = json.loads(vault_credentials_stdout)
    except json.decoder.JSONDecodeError:
        print("CRIT: Are you logged in vault?")
        sys.exit(1)
    return credentials


def get_subs_name(do_print=False) -> str:
    """Return the working subscription name."""
    state_file_path = f"{os.path.dirname(__file__)}/.subs_name"
    if os.path.isfile(state_file_path):
        with open(state_file_path, "r") as state_file:
            subs_name: str = state_file.read()
    else:
        print("CRIT: You must set the subscription name first.")
        sys.exit(1)
    if do_print:
        print(f"INFO: Working on {subs_name}.")
    return subs_name


def get_user_name(do_print=False) -> str:
    """Return the working user name."""
    state_file_path = f"{os.path.dirname(__file__)}/.user_name"
    if os.path.isfile(state_file_path):
        with open(state_file_path, "r") as state_file:
            user_name: str = state_file.read()
    else:
        print("CRIT: You must set the user name first.")
        sys.exit(1)
    if do_print:
        print(f"INFO: Working as {user_name}.")
    return user_name


def get_files_with_state(file_state: str) -> None:
    """Print all files with file_state."""
    credentials: JSON = get_credentials()
    subs_name: str = get_subs_name()

    print(f"INFO: For subscription {subs_name}, files marked as {file_state}:")
    for repo_name, file_path, file_lines, file_last_hash in \
            row__data__get_all_with_state(credentials, subs_name, file_state):
        print(
            f"{repo_name}/{file_path} ({file_lines} lines) [{file_last_hash}]")


def get_coverage(all_subs: bool = True) -> None:
    """Compute the coverage for one or all groups."""
    if all_subs:
        previous_subs_name: str = get_subs_name()
        credentials: JSON = get_credentials()
        for subs_name in get_all_groups(credentials):
            set_subs_name(subs_name)
            get_coverage(all_subs=False)
        set_subs_name(previous_subs_name)
        return

    credentials = get_credentials()

    subs_name = get_subs_name()

    datas: Any = {}
    for repo_name, _, file_lines, _ in \
            row__data__get_all_with_state(credentials, subs_name, "tainted"):
        try:
            datas[repo_name]["tainted"] += file_lines
        except KeyError:
            datas[repo_name] = {"tainted": file_lines, "clean": 0}

    for repo_name, _, file_lines, _ in \
            row__data__get_all_with_state(credentials, subs_name, "clean"):
        try:
            datas[repo_name]["clean"] += file_lines
        except KeyError:
            datas[repo_name] = {"clean": file_lines, "tainted": 0}

    get_coverage__print_header(
        subs_name, "Coverage")
    subs_total_clean = 0
    subs_total_tainted = 0
    for repo_name in datas:
        repo_total_clean = datas[repo_name]["clean"]
        repo_total_tainted = datas[repo_name]["tainted"]
        subs_total_clean += repo_total_clean
        subs_total_tainted += repo_total_tainted
        get_coverage__print_coverage(
            repo_name, repo_total_clean, repo_total_tainted)
    get_coverage__print_hor_line()
    get_coverage__print_coverage(
        "Total", subs_total_clean, subs_total_tainted)
    get_coverage__print_hor_line()
    print()


def get_coverage__print_coverage(source: str, clean: int, tainted: int):
    """Print a line of coverage to stdout."""
    coverage = 100.0 * clean / (clean + tainted)
    print(
        "|{:^64s}| {:>12d} / {:>12d} ({:>5.1f}%) |".format(
            source[-64:], clean, tainted, coverage))


def get_coverage__print_hor_line():
    """Print an horizontal line to stdout."""
    print("-" * 105)


def get_coverage__print_header(*args):
    """Print a header to stdout."""
    get_coverage__print_hor_line()
    print("|{:^64s}|{:^38s}|".format(*args))
    get_coverage__print_hor_line()


def set_subs_name(subs_name: str) -> None:
    """Set the working subscription name."""
    state_file_path = f"{os.path.dirname(__file__)}/.subs_name"
    with open(state_file_path, "w") as state_file:
        state_file.write(subs_name)
        print(f"INFO: Subscription name set to {subs_name}.")


def set_user_name(user_name: str) -> None:
    """Set the working user name."""
    state_file_path = f"{os.path.dirname(__file__)}/.user_name"
    with open(state_file_path, "w") as state_file:
        state_file.write(user_name)
        print(f"INFO: User name set to {user_name}.")


def set_file_state(
        repo_name: str,
        file_path: str,
        file_state_new: str,
        comfirmation: bool = False) -> None:
    """Mark a file as tainted."""
    credentials: JSON = get_credentials()
    subs_name: str = get_subs_name()
    user_name: str = get_user_name()

    print(f"Attemting to mark as {file_state_new}:")
    print(f"  subs_name:      {subs_name}")
    print(f"  repo_name:      {repo_name}")
    print(f"  file_path:      {file_path}")
    file_lines, file_state, file_last_hash = \
        row__data__get_by_index(credentials, subs_name, repo_name, file_path)
    if file_state:
        print(f"  file_lines:     {file_lines}")
        print(f"  file_state:     {file_state}")
        print(f"  file_last_hash: {file_last_hash}")
        if comfirmation or input("Type 'yes' to confirm: ") == "yes":
            row__data__upsert(
                credentials,
                subs_name,
                repo_name,
                file_path,
                file_lines,
                file_state_new,
                file_last_hash)
            row__logs__insert(
                credentials,
                "new state",
                user_name,
                subs_name,
                repo_name,
                file_path,
                file_lines,
                file_state_new,
                file_last_hash)
            print("INFO: Done.")
    else:
        print("WARN: You can not modify non-existing rows.")


def main():
    """Usual entry point."""
    # command line interface
    args: Iterable[str] = iter(sys.argv[1:])
    argv: List[str] = [next(args, "") for _ in range(0, 4)]

    # parse arguments
    if main__parse_set(*argv) or \
            main__parse_get(*argv) or \
            main__parse_admin(*argv):
        sys.exit(0)
    else:
        print_tutorial()


def main__parse_set(cmd: str, arg1: str, arg2: str, arg3: str) -> bool:
    """Parse the CLI set group."""
    was_captured: bool = True
    if cmd == "set" and arg1 == "subscription":
        subs_name = arg2
        set_subs_name(subs_name)
    elif cmd == "set" and arg1 == "username":
        user_name = arg2
        set_user_name(user_name)
    elif cmd == "set" and arg1 == "tainted":
        repo_name = arg2
        file_path = arg3
        set_file_state(repo_name, file_path, "tainted")
    elif cmd == "set" and arg1 == "clean":
        repo_name = arg2
        file_path = arg3
        set_file_state(repo_name, file_path, "clean")
    else:
        was_captured = False
    return was_captured


def main__parse_get(cmd: str, arg1: str, arg2: str, arg3: str) -> bool:
    """Parse the CLI get group."""
    was_captured: bool = True
    if cmd == "get" and arg1 == "configurations":
        get_subs_name(do_print=True)
        get_user_name(do_print=True)
    elif cmd == "get" and arg1 == "tainted":
        get_files_with_state("tainted")
    elif cmd == "get" and arg1 == "clean":
        get_files_with_state("clean")
    elif cmd == "get" and arg1 == "coverage":
        get_coverage(all_subs=False)
    elif cmd == "get" and arg1 == "coverages":
        get_coverage(all_subs=True)
    else:
        was_captured = False
    return was_captured


def main__parse_admin(cmd: str, arg1: str, arg2: str, arg3: str) -> bool:
    """Parse the CLI admin group."""
    was_captured: bool = True
    if cmd == "database" and arg1 == "init":
        database_init()
    elif cmd == "database" and arg1 == "push" and arg2:
        repo_path = os.path.abspath(arg2)
        database_push(repo_path)
    elif cmd == "database" and arg1 == "wring" and arg2:
        lines_csv_path = os.path.abspath(arg2)
        database_wring(lines_csv_path)
    elif cmd == "database" and arg1 == "remove" and arg2 == "repository":
        repo_name = arg3
        database_remove_repository(repo_name)
    elif cmd == "database" and arg1 == "vacuum":
        database_vacuum()
    else:
        was_captured = False
    return was_captured


if __name__ == "__main__":
    main()
