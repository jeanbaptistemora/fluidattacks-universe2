"""
Singer tap for a git repository
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import os
import re
import json
import argparse
import datetime

from typing import Tuple, Any

import git

# Type aliases that improve clarity
JSON = Any
GIT_REPO = Any
GIT_COMMIT = Any

def sprint(json_obj: JSON) -> None:
    """Prints a JSON object to stdout.
    """

    print(json.dumps(json_obj))


def parse_actors(path: str, sha1: str) -> Tuple[str, str, str, str]:
    """Returns author name/email and commiter name/email.

    Args:
        path: The path to the repository.
        sha1: The SHA1 of the commit.

    Returns:
        A tuple of authors/committers names/emails.

    The quality of this function is upto the .mailmap.
    """

    authorn: str = os.popen((
        f"cd '{path}';"
        f"git --no-pager show -s --format='%aN' {sha1}")).read()[0:-1]
    authore: str = os.popen((
        f"cd '{path}';"
        f"git --no-pager show -s --format='%aE' {sha1}")).read()[0:-1]
    commitn: str = os.popen((
        f"cd '{path}';"
        f"git --no-pager show -s --format='%cN' {sha1}")).read()[0:-1]
    commite: str = os.popen((
        f"cd '{path}';"
        f"git --no-pager show -s --format='%cE' {sha1}")).read()[0:-1]
    return authorn, authore, commitn, commite


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


def get_extension(file_name):
    """ returns the extension of a file """
    tokens = file_name.split(".")
    return tokens[-1].lower() if len(tokens) > 1 else "none"


def changes_table(last_commit, commit, files):
    """ writes singer records to stdout

        analytics of every commit yields a side-efect that is the "changes" table
        this table contains detailed information about the files touched by a commit """

    def base_srecord():
        """ returns a basic singer record """
        srecord = {
            "type": "RECORD",
            "stream": "changes",
            "record": {
                "sha1": commit.hexsha,
            }
        }
        return srecord

    diff = last_commit.diff(commit)

    def getstats(stats):
        """ return a little dict with stats """
        insertions = stats["insertions"]
        deletions = stats["deletions"]
        ret = {
            "insertions": insertions,
            "deletions": deletions,
            "tot_lines": insertions + deletions,
            "net_lines": insertions - deletions,
        }
        return ret

    # ’A’ for added paths
    for file in diff.iter_change_type("A"):
        srecord = base_srecord()
        srecord["record"]["type"] = "add"
        srecord["record"]["target_path"] = file.b_path
        srecord["record"]["target_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        sprint(srecord)
    # ’D’ for deleted paths
    for file in diff.iter_change_type("D"):
        srecord = base_srecord()
        srecord["record"]["type"] = "del"
        srecord["record"]["target_path"] = file.a_path
        srecord["record"]["target_ext"] = get_extension(file.a_path)
        if file.a_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.a_path])}
        sprint(srecord)
    # ’R’ for renamed paths
    for file in diff.iter_change_type("R"):
        srecord = base_srecord()
        srecord["record"]["type"] = "ren"
        srecord["record"]["source_path"] = file.rename_from
        srecord["record"]["source_ext"] = get_extension(file.rename_from)
        srecord["record"]["target_path"] = file.rename_to
        srecord["record"]["target_ext"] = get_extension(file.rename_to)
        for file_name, stats in files.items():
            weird = re.sub(r"(.*){(.*) => (.*)}(.*)", r"\g<1>\g<3>\g<4>", file_name)
            if weird == file.rename_to:
                srecord["record"] = {**srecord["record"], **getstats(stats)}
        sprint(srecord)
    # ’M’ for paths with modified data
    for file in diff.iter_change_type("M"):
        srecord = base_srecord()
        srecord["record"]["type"] = "mod"
        srecord["record"]["target_path"] = file.b_path
        srecord["record"]["target_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        sprint(srecord)
    # ’T’ for changed in the type paths
    for file in diff.iter_change_type("T"):
        srecord = base_srecord()
        srecord["record"]["type"] = "modtype"
        srecord["record"]["target_path"] = file.b_path
        srecord["record"]["target_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        sprint(srecord)


def scan_commits(config, sync_changes, after):
    """ extracts all information possible from the commit object """

    # must have
    repository = config["repository"]
    branches = config["branches"]
    repo_path = config["location"]
    repo_obj = git.Repo(repo_path)

    # optional
    organization = config.get("organization", "__")
    subscription = config.get("subscription", "__")
    tag = config.get("tag", "__")

    def write_schemas():
        """ writes singer schemas to stdout """
        schemas = [
            "commits.schema.json",
            "changes.schema.json"
        ]
        for schema in schemas:
            with open(f"{os.path.dirname(__file__)}/{schema}", "r") as file:
                sprint(json.load(file))

    def write_records(branch):
        """ writes singer records to stdout """

        last_commit = None
        # iterate from first to latest
        # test kwargs mangling in this function: git.cmd.Git().transform_kwargs()
        for commit in repo_obj.iter_commits(
                branch,
                date="iso-strict",
                after=after,
                reverse=True,
                no_merges=True):
            commit_insertions = commit.stats.total.get("insertions", 0)
            commit_deletions = commit.stats.total.get("deletions", 0)

            # Gitpython don't parse it correctly
            #authorn, authore = commit.author.name, commit.author.email
            #commitn, commite = commit.committer.name, commit.committer.email

            # let's parse it ourselves
            authorn, authore, commitn, commite = parse_actors(repo_path, commit.hexsha)

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
                    "authored_at": commit.authored_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "committed_at": commit.committed_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "summary": commit.summary,
                    "message": re.sub(r"^[\n\r]*", "", commit.message.replace(commit.summary, "")),
                    "commit_files": commit.stats.total.get("files", 0),
                    "commit_insertions": commit_insertions,
                    "commit_deletions": commit_deletions,
                    "commit_tot_lines": commit_insertions + commit_deletions,
                    "commit_net_lines": commit_insertions - commit_deletions
                }
            }

            sprint(srecord)

            if sync_changes and not last_commit is None:
                changes_table(last_commit, commit, commit.stats.files)

            last_commit = commit

    write_schemas()

    for branch in branches:
        write_records(branch)


def get_chunk(iterable, nchunks, chunk_id):
    """Returns the n-th chunk of an iterable.
    """

    schunk = len(iterable) // nchunks + 1
    beg = (chunk_id - 1) * schunk
    end = (chunk_id - 0) * schunk

    return iterable[beg:] if chunk_id == nchunks else iterable[beg:end]


def main():
    """Usual entry point.
    """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--conf',
        required=True,
        help='JSON configuration file',
        type=argparse.FileType('r'),
        dest="conf")
    parser.add_argument(
        '--last-n-days',
        help='in days (positive) how many days to go back and sync',
        type=int,
        dest="this_days",
        default=36500)
    parser.add_argument(
        '--no-changes',
        help='flag to indicate if changes table should not be generated',
        action='store_false',
        dest="sync_changes",
        default=True)
    parser.add_argument(
        '--threads',
        help='=the number of processes to fork in',
        type=int,
        dest="nthreads",
        default=1)
    parser.add_argument(
        '--fork-id',
        help='=the id of the current fork',
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
        try:
            # pylint: disable=broad-except
            scan_commits(conf, args.sync_changes, after)
        except Exception as excp:
            sprint({"type": "STATE", "value": str(excp)})


if __name__ == "__main__":
    main()
