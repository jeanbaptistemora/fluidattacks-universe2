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

# pylint: disable=import-error
import git

SPRINT = lambda s: print(json.dumps(s))

def get_extension(file_name):
    """ returns the extension of a file """
    tokens = file_name.split(".")
    return tokens[-1].lower() if len(tokens) > 1 else "none"

def changes_table(repo_name, branch, last_commit, commit, files):
    """ writes singer records to stdout

        analytics of every commit yields a side-efect that is the "changes" table
        this table contains detailed information about the files touched by a commit """

    def base_srecord():
        """ returns a basic singer record """
        srecord = {
            "type": "RECORD",
            "stream": "changes",
            "record": {
                "repo_name": repo_name,
                "branch": branch,
                "sha1": commit.hexsha,
                "sha1_short": commit.hexsha[0:7]
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
            "total_deltas": insertions + deletions,
            "net_deltas": insertions - deletions,
        }
        return ret

    # ’A’ for added paths
    for file in diff.iter_change_type("A"):
        srecord = base_srecord()
        srecord["record"]["add"] = file.b_path
        srecord["record"]["add_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        SPRINT(srecord)
    # ’D’ for deleted paths
    for file in diff.iter_change_type("D"):
        srecord = base_srecord()
        srecord["record"]["del"] = file.a_path
        srecord["record"]["del_ext"] = get_extension(file.a_path)
        if file.a_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.a_path])}
        SPRINT(srecord)
    # ’R’ for renamed paths
    for file in diff.iter_change_type("R"):
        srecord = base_srecord()
        srecord["record"]["ren_from"] = file.rename_from
        srecord["record"]["ren_from_ext"] = get_extension(file.rename_from)
        srecord["record"]["ren_to"] = file.rename_to
        srecord["record"]["ren_to_ext"] = get_extension(file.rename_to)
        for file_name, stats in files.items():
            weird = re.sub(r"(.*){(.*) => (.*)}(.*)", r"\g<1>\g<3>\g<4>", file_name)
            if weird == file.rename_to:
                srecord["record"] = {**srecord["record"], **getstats(stats)}
        SPRINT(srecord)
    # ’M’ for paths with modified data
    for file in diff.iter_change_type("M"):
        srecord = base_srecord()
        srecord["record"]["mod"] = file.b_path
        srecord["record"]["mod_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        SPRINT(srecord)
    # ’T’ for changed in the type paths
    for file in diff.iter_change_type("T"):
        srecord = base_srecord()
        srecord["record"]["modtype"] = file.b_path
        srecord["record"]["modtype_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        SPRINT(srecord)

def scan_commits(repo_name, repo_obj, branches):
    """ extracts all information possible from the commit object """

    def write_schemas():
        """ writes singer schemas to stdout """
        schemas = [
            "commits.schema.json",
            "changes.schema.json"
        ]
        for schema in schemas:
            with open(f"{os.path.dirname(__file__)}/{schema}", "r") as file:
                SPRINT(json.load(file))

    def write_records(branch):
        """ writes singer records to stdout """

        skip = 0
        last_commit = None
        # iterate from first to latest
        for commit in repo_obj.iter_commits(branch, skip=skip, reverse=True):
            total_insertions = commit.stats.total.get("insertions", 0)
            total_deletions = commit.stats.total.get("deletions", 0)

            srecord = {
                "type": "RECORD",
                "stream": "commits",
                "record": {
                    "repo_name": repo_name,
                    "branch": branch,
                    "sha1": commit.hexsha,
                    "sha1_short": commit.hexsha[0:7],
                    "author_name": commit.author.name,
                    "author_email": commit.author.email,
                    "committer_name": commit.committer.name,
                    "committer_email": commit.committer.email,
                    "authored_at": commit.authored_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "committed_at": commit.committed_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "summary": commit.summary,
                    "message": re.sub(r"^[\n\r]*", "", commit.message.replace(commit.summary, "")),
                    "total_files": commit.stats.total.get("files", 0),
                    "total_lines": commit.stats.total.get("lines", 0),
                    "total_insertions": total_insertions,
                    "total_deletions": total_deletions,
                    "net_lines": total_insertions - total_deletions
                }
            }

            SPRINT(srecord)

            if not last_commit is None:
                changes_table(repo_name, branch, last_commit, commit, commit.stats.files)

            last_commit = commit

            skip += 1

    write_schemas()

    for branch in branches:
        write_records(branch)

def main():
    """ usual entry point """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--conf',
        required=True,
        help='JSON configuration file',
        type=argparse.FileType('r'),
        dest="conf")
    parser.add_argument(
        '-s', '--state',
        help='JSON state file',
        type=argparse.FileType('r'),
        dest="state")
    args = parser.parse_args()

    confs = json.load(args.conf)

    for repo_name, conf in confs.items():
        repo_obj = git.Repo(conf["location"])

        scan_commits(repo_name, repo_obj, conf["branches"])

if __name__ == "__main__":
    main()
