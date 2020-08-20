#!/usr/bin/env python3

"""Singer tap for a git repository."""

import os
import re
import sys
import json
import argparse
import datetime

from typing import List, Tuple, Any

import git

from . import dags
from . import metrics
from . import os_tools

# Type aliases that improve clarity
JSON = Any
GIT_REPO = Any
GIT_COMMIT = Any


def sprint(json_obj: JSON) -> None:
    """Prints a JSON object to stdout."""
    print(json.dumps(json_obj))


def print_stderr(*args: Any) -> None:
    """Print to stderr and flush the buffer."""
    print(*args, file=sys.stderr, flush=True)


def go_back(this_days: int) -> str:
    """Returns today minus this_days as a RFC339 string.

    Fixes possible overflows.
    """
    # minimum date to be used is 1970-01-01T00:00:01 (UTC)
    lower_limit = datetime.datetime.utcfromtimestamp(1)

    # maximum date to be used is 2038-01-19T03:14:07 (UTC)
    upper_limit = datetime.datetime.utcfromtimestamp(2147483647)

    # the date the user provided
    now = datetime.datetime.now() + datetime.timedelta(-1 * this_days)

    # fix the possible overflow (timestamp as 32bit signed integer in C-lang)
    now = lower_limit if now < lower_limit else now
    now = upper_limit if now > upper_limit else now

    # everything fine now
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_extension(file_name: str) -> str:
    """Returns the extension of a file."""
    tokens = file_name.split(".")
    return tokens[-1].lower() if len(tokens) > 1 else "none"


def get_chunk(iterable: List[Any], nchunks: int, chunk_id: int) -> List[Any]:
    """Returns the n-th chunk of an iterable."""
    schunk = len(iterable) // nchunks + 1
    beg = (chunk_id - 1) * schunk
    end = (chunk_id - 0) * schunk

    return iterable[beg:] if chunk_id == nchunks else iterable[beg:end]


def parse_actors(path: str, sha1: str) -> Tuple[str, str, str, str]:
    """Returns author name/email and commiter name/email.

    Args:
        path: The path to the repository.
        sha1: The SHA1 of the commit.

    Returns:
        A tuple of authors/committers names/emails.

    The quality of this function is upto the .mailmap.
    """
    authorn: str = os_tools.get_stdout_stderr(
        [
            "git", "-C", path,
            "--no-pager", "show", "-s", "--format=%aN", sha1])[0][0:-1]
    authore: str = os_tools.get_stdout_stderr(
        [
            "git", "-C", path,
            "--no-pager", "show", "-s", "--format=%aE", sha1])[0][0:-1]
    commitn: str = os_tools.get_stdout_stderr(
        [
            "git", "-C", path,
            "--no-pager", "show", "-s", "--format=%cN", sha1])[0][0:-1]
    commite: str = os_tools.get_stdout_stderr(
        [
            "git", "-C", path,
            "--no-pager", "show", "-s", "--format=%cE", sha1])[0][0:-1]
    return authorn, authore, commitn, commite


def scan_commits(config: JSON, sync_changes: bool, after: str) -> None:
    """Wrings all information possible from the commit object."""

    # must have
    repository: str = config["repository"]
    repo_path: str = config["location"]
    branches: str = config["branches"]
    repo_obj: GIT_REPO = git.Repo(repo_path)

    # optional
    organization: str = config.get("organization", "__")
    subscription: str = config.get("subscription", "__")
    tag: str = config.get("tag", "__")

    # set the rename limit
    os.system(f"git -C {repo_path} config --int diff.renameLimit 16384")

    # get DAG properties
    analized_dag = dags.get_commits(repo_path)

    def write_records(branch):
        """Print singer records to stdout."""
        last_commit = None
        for commit in repo_obj.iter_commits(
                branch,
                after=after,
                reverse=True,
                no_merges=True,
                date="iso-strict"):
            commit_insertions = commit.stats.total.get("insertions", 0)
            commit_deletions = commit.stats.total.get("deletions", 0)

            # maybe some day Gitpython will do it correctly
            # authorn, authore = commit.author.name, commit.author.email
            # commitn, commite = commit.committer.name, commit.committer.email
            authorn, authore, commitn, commite = parse_actors(
                repo_path, commit.hexsha)

            srecord = {
                "type": "RECORD",
                "stream": "commits",
                "record": {
                    "organization": organization,
                    "subscription": subscription,
                    "repository": repository,
                    "tag": tag,
                    "branch": branch,
                    "sha1": commit.hexsha,
                    "sha1_short": commit.hexsha[0:7],
                    "author_name": authorn,
                    "author_email": authore,
                    "committer_name": commitn,
                    "committer_email": commite,
                    "authored_at": commit.authored_datetime.strftime(
                        "%Y-%m-%dT%H:%M:%SZ"),
                    "committed_at": commit.committed_datetime.strftime(
                        "%Y-%m-%dT%H:%M:%SZ"),
                    "integration_authored_at": analized_dag[commit.hexsha][
                        "integration_authored_at"].strftime(
                            "%Y-%m-%dT%H:%M:%SZ"),
                    "integration_committed_at": analized_dag[commit.hexsha][
                        "integration_committed_at"].strftime(
                            "%Y-%m-%dT%H:%M:%SZ"),
                    "time_to_master_authored": analized_dag[commit.hexsha][
                        "time_to_master_authored"],
                    "time_to_master_committed": analized_dag[commit.hexsha][
                        "time_to_master_committed"],
                    "summary": commit.summary,
                    "message": re.sub(r"^[\n\r]*", "", commit.message.replace(
                        commit.summary, "")),
                    "commit_files": commit.stats.total.get("files", 0),
                    "commit_insertions": commit_insertions,
                    "commit_deletions": commit_deletions,
                    "commit_tot_lines": commit_insertions + commit_deletions,
                    "commit_net_lines": commit_insertions - commit_deletions
                }
            }

            sprint(srecord)

            if sync_changes and last_commit is not None:
                scan_changes(last_commit, commit, commit.stats.files)

            last_commit = commit

    scan_commits__schemas(sync_changes)

    for branch in branches:
        write_records(branch)


def scan_commits__schemas(sync_changes: bool):
    """Prints schemas to stdout."""
    schemas = ["commits.schema.json"]
    if sync_changes:
        schemas.append("changes.schema.json")
    for schema in schemas:
        with open(f"{os.path.dirname(__file__)}/{schema}", "r") as file:
            sprint(json.load(file))


def scan_changes(
        prev_commit: GIT_COMMIT,
        this_commit: GIT_COMMIT,
        files: JSON) -> None:
    """Writes singer records for the changes table to stdout.

    Comparison between two succesive commits yields a table of changes.

    This table contains information about every file touched by a commit.
    """

    diff = prev_commit.diff(this_commit)

    for file in diff.iter_change_type("A"):
        scan_changes__type_a(file, files, this_commit)
    for file in diff.iter_change_type("D"):
        scan_changes__type_d(file, files, this_commit)
    for file in diff.iter_change_type("R"):
        scan_changes__type_r(file, files, this_commit)
    for file in diff.iter_change_type("M"):
        scan_changes__type_m(file, files, this_commit)
    for file in diff.iter_change_type("T"):
        scan_changes__type_t(file, files, this_commit)


def scan_changes__base_record(commit: GIT_COMMIT) -> JSON:
    """Returns a basic singer record."""
    base_record = {
        "type": "RECORD",
        "stream": "changes",
        "record": {
            "sha1": commit.hexsha,
        }
    }
    return base_record


def scan_changes__insert_stats(record: JSON, stats: JSON) -> JSON:
    """Adds the stats to the record."""
    insertions = stats["insertions"]
    deletions = stats["deletions"]
    record["record"]["insertions"] = insertions
    record["record"]["deletions"] = deletions
    record["record"]["tot_lines"] = insertions + deletions
    record["record"]["net_lines"] = insertions - deletions


def scan_changes__type_a(file, files: JSON, this_commit: GIT_COMMIT) -> None:
    """Handles the scanning of added paths."""
    record = scan_changes__base_record(this_commit)
    record["record"]["type"] = "add"
    record["record"]["target_path"] = file.b_path
    record["record"]["target_ext"] = get_extension(file.b_path)
    if file.b_path in files:
        scan_changes__insert_stats(record, files[file.b_path])
    sprint(record)


def scan_changes__type_d(file, files: JSON, this_commit: GIT_COMMIT) -> None:
    """Handles the scanning of deleted paths."""
    srecord = scan_changes__base_record(this_commit)
    srecord["record"]["type"] = "del"
    srecord["record"]["target_path"] = file.a_path
    srecord["record"]["target_ext"] = get_extension(file.a_path)
    if file.a_path in files:
        scan_changes__insert_stats(srecord, files[file.a_path])
    sprint(srecord)


def scan_changes__type_r(file, files: JSON, this_commit: GIT_COMMIT) -> None:
    """Handles the scanning of renamed files."""
    srecord = scan_changes__base_record(this_commit)
    srecord["record"]["type"] = "ren"
    srecord["record"]["source_path"] = file.rename_from
    srecord["record"]["source_ext"] = get_extension(file.rename_from)
    srecord["record"]["target_path"] = file.rename_to
    srecord["record"]["target_ext"] = get_extension(file.rename_to)
    for file_name, stats in files.items():
        weird = re.sub(
            r"(.*){(.*) => (.*)}(.*)",
            r"\g<1>\g<3>\g<4>",
            file_name)
        if weird == file.rename_to:
            scan_changes__insert_stats(srecord, stats)
    sprint(srecord)


def scan_changes__type_m(file, files: JSON, this_commit: GIT_COMMIT) -> None:
    """Handles the scanning of file changed on modified data."""
    srecord = scan_changes__base_record(this_commit)
    srecord["record"]["type"] = "mod"
    srecord["record"]["target_path"] = file.b_path
    srecord["record"]["target_ext"] = get_extension(file.b_path)
    if file.b_path in files:
        scan_changes__insert_stats(srecord, files[file.b_path])
    sprint(srecord)


def scan_changes__type_t(file, files: JSON, this_commit: GIT_COMMIT) -> None:
    """Handles the scanning of file changed in the type."""
    srecord = scan_changes__base_record(this_commit)
    srecord["record"]["type"] = "modtype"
    srecord["record"]["target_path"] = file.b_path
    srecord["record"]["target_ext"] = get_extension(file.b_path)
    if file.b_path in files:
        scan_changes__insert_stats(srecord, files[file.b_path])
    sprint(srecord)


def scan_gitinspector(path: str) -> JSON:
    """Creates the gitinspector table."""
    output: str = os.popen((
        f"gitinspector             "
        f"  --responsibilities=true"
        f"  --timeline=true        "
        f"  --metrics=true         "
        f"  --format=json          "
        f"  --hard                 "
        f"  '{path}'               ")).read()

    data = json.loads(output)["gitinspector"]
    scan_gitinspector__schemas()
    scan_gitinspector__blame(data)
    scan_gitinspector__changes(data)
    scan_gitinspector__metrics(data)
    scan_gitinspector__responsibilities(data)


def scan_gitinspector__schemas() -> None:
    """Print to stdout the schemas."""
    schemas = (
        "gitinspector_blame.schema.json",
        "gitinspector_changes.schema.json",
        "gitinspector_metrics.schema.json",
        "gitinspector_responsibilities.schema.json",
    )
    for schema in schemas:
        with open(f"{os.path.dirname(__file__)}/{schema}", "r") as file:
            sprint(json.load(file))


def scan_gitinspector__blame(data: JSON) -> None:
    """Print to stdout records for the blame table."""
    if "blame" in data and "authors" in data["blame"]:
        for record in data["blame"]["authors"]:
            srecord = {
                "type": "RECORD",
                "stream": "gitinspector_blame",
                "record": {
                    "repository": data["repository"],
                    "name": record["name"],
                    "email": record["email"],
                    "rows": record["rows"],
                    "stability": record["stability"],
                    "age": record["age"],
                    "percentage_in_comments": record["percentage_in_comments"],
                }
            }
            sprint(srecord)


def scan_gitinspector__changes(data: JSON) -> None:
    """Print to stdout records for the changes table."""
    if "changes" in data and "authors" in data["changes"]:
        for record in data["changes"]["authors"]:
            srecord = {
                "type": "RECORD",
                "stream": "gitinspector_changes",
                "record": {
                    "repository": data["repository"],
                    "name": record["name"],
                    "email": record["email"],
                    "commits": record["commits"],
                    "insertions": record["insertions"],
                    "deletions": record["deletions"],
                    "percentage_of_changes": record["percentage_of_changes"],
                }
            }
            sprint(srecord)


def scan_gitinspector__metrics(data: JSON) -> None:
    """Print to stdout records for the metrics table."""
    if "metrics" in data and "violations" in data["metrics"]:
        for record in data["metrics"]["violations"]:
            srecord = {
                "type": "RECORD",
                "stream": "gitinspector_metrics",
                "record": {
                    "repository": data["repository"],
                    "type": record["type"],
                    "file_name": record["file_name"],
                    "value": record["value"],
                }
            }
            sprint(srecord)


def scan_gitinspector__responsibilities(data: JSON) -> None:
    """Print to stdout records for the responsibilities table."""
    if "responsibilities" in data and "authors" in data["responsibilities"]:
        for record in data["responsibilities"]["authors"]:
            if "files" in record:
                for file in record["files"]:
                    srecord = {
                        "type": "RECORD",
                        "stream": "gitinspector_responsibilities",
                        "record": {
                            "repository": data["repository"],
                            "name": record["name"],
                            "email": record["email"],
                            "files_name": file["name"],
                            "files_rows": file["rows"],
                        }
                    }
                    sprint(srecord)


def main():
    """Usual entry point."""
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--conf',
        required=True,
        help='JSON configuration file.',
        type=argparse.FileType('r'),
        dest="conf")
    parser.add_argument(
        '--last-n-days',
        help='in days (positive) how many days to go back and sync.',
        type=int,
        dest="this_days",
        default=36500)
    parser.add_argument(
        '--no-changes',
        help='flag to indicate if changes table should not be generated.',
        action='store_false',
        dest="sync_changes",
        default=True)
    parser.add_argument(
        '--run-gitinspector',
        help='flag to indicate if gitinspector should be ran.',
        action='store_true',
        dest="run_gitinspector",
        default=False)
    parser.add_argument(
        '--with-metrics',
        help='flag to indicate if metrics should be generated.',
        action='store_true',
        dest="with_metrics",
        default=False)
    parser.add_argument(
        '--threads',
        help='=the number of processes to fork in.',
        type=int,
        dest="nthreads",
        default=1)
    parser.add_argument(
        '--fork-id',
        help='=the id of the current fork.',
        type=int,
        dest="fork_id",
        default=1)
    args = parser.parse_args()

    # catch the config file (JSON) (list<dict>)
    configs = json.load(args.conf)
    # divide it into chunks, and pick the n-th chunk
    configs = get_chunk(configs, args.nthreads, args.fork_id)
    # now process that chunk

    # we are going to fetch commits since this date
    after = go_back(args.this_days)

    for conf in configs:
        repository = conf["repository"]

        # pylint: disable=broad-except
        if args.run_gitinspector:
            try:
                scan_gitinspector(conf["location"])
            except Exception as excp:
                print_stderr(
                    f"EXCP: scan_gitinspector {repository}.", repr(excp))

        if args.with_metrics:
            try:
                metrics.scan_metrics(conf["repository"], conf["location"])
            except Exception as excp:
                print_stderr(
                    f"WARN: metrics.scan_metrics {repository}.", repr(excp))

        try:
            scan_commits(conf, args.sync_changes, after)
        except Exception as excp:
            print_stderr(
                f"WARN: scan_commits {repository}.", repr(excp))


if __name__ == "__main__":
    main()
