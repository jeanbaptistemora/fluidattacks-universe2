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

def line_iter(file_path):
    """ iterator to the lines of a file """
    with open(file_path, "r") as file:
        line = file.readline()
        while line:
            yield line
            line = file.readline()

def load_mailmap(mailmap_path):
    """ loads a .mailmap into a fast datastructure """

    # pylint: disable=C0103
    # N = canonical name
    # E = canonical email
    # n = git name
    # e = git email
    # _ = anything

    mm_structure = []

    for line in line_iter(mailmap_path):
        statement = re.sub(r"\s+", " ", line)
        NEne = re.match(r"(.*) <(.*)> (.*) <(.*)>", statement)
        NE_e = re.match(r"(.*) <(.*)> <(.*)>", statement)
        _E_e = re.match(r"<(.*)> <(.*)>", statement)
        N__e = re.match(r"(.*) <(.*)>", statement)

        if NEne:
            groups = NEne.groups()
            mm_structure.append((groups[0], groups[1], groups[2], groups[3]))
        elif NE_e:
            groups = NE_e.groups()
            mm_structure.append((groups[0], groups[1], None, groups[2]))
        elif _E_e:
            groups = _E_e.groups()
            mm_structure.append((None, groups[0], None, groups[1]))
        elif N__e:
            groups = N__e.groups()
            mm_structure.append((groups[0], None, None, groups[1]))

    return mm_structure

def replace_mailmap(user_n, user_e, mailmap):
    """ uses the list of tuples generated in load_mailmap to return canonical name and email """

    # pylint: disable=C0103
    # N = canonical name
    # E = canonical email
    # n = git name
    # e = git email
    # _ = anything

    user_N, user_E = user_n, user_e
    for N, E, n, e in mailmap:
        # NEne
        if user_n == n and user_e == e:
            user_N, user_E = N, E
        # NE_e
        if n is None and user_e == e:
            user_N, user_E = N, E
        # _E_e
        if N is None and n is None and user_e == e:
            user_E = E
        # N__e
        if E is None and n is None and user_e == e:
            user_N = N
    return (user_N, user_E)

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
            "total_deltas": insertions + deletions,
            "net_deltas": insertions - deletions,
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
        SPRINT(srecord)
    # ’D’ for deleted paths
    for file in diff.iter_change_type("D"):
        srecord = base_srecord()
        srecord["record"]["type"] = "del"
        srecord["record"]["target_path"] = file.a_path
        srecord["record"]["target_ext"] = get_extension(file.a_path)
        if file.a_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.a_path])}
        SPRINT(srecord)
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
        SPRINT(srecord)
    # ’M’ for paths with modified data
    for file in diff.iter_change_type("M"):
        srecord = base_srecord()
        srecord["record"]["type"] = "mod"
        srecord["record"]["target_path"] = file.b_path
        srecord["record"]["target_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        SPRINT(srecord)
    # ’T’ for changed in the type paths
    for file in diff.iter_change_type("T"):
        srecord = base_srecord()
        srecord["record"]["type"] = "modtype"
        srecord["record"]["target_path"] = file.b_path
        srecord["record"]["target_ext"] = get_extension(file.b_path)
        if file.b_path in files:
            srecord["record"] = {**srecord["record"], **getstats(files[file.b_path])}
        SPRINT(srecord)

def scan_commits(repo_name, config, mailmap, sync_changes):
    """ extracts all information possible from the commit object """

    repo_obj = git.Repo(config["location"])
    group = config.get("group", "__")
    branches = config["branches"]

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

        last_commit = None
        # iterate from first to latest
        for commit in repo_obj.iter_commits(branch, reverse=True):
            total_insertions = commit.stats.total.get("insertions", 0)
            total_deletions = commit.stats.total.get("deletions", 0)

            authorn, authore = commit.author.name, commit.author.email
            commitn, commite = commit.committer.name, commit.committer.email

            authorn, authore = replace_mailmap(authorn, authore, mailmap)
            commitn, commite = replace_mailmap(commitn, commite, mailmap)

            srecord = {
                "type": "RECORD",
                "stream": "commits",
                "record": {
                    "group": group,
                    "repo_name": repo_name,
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
                    "total_files": commit.stats.total.get("files", 0),
                    "total_lines": commit.stats.total.get("lines", 0),
                    "total_insertions": total_insertions,
                    "total_deletions": total_deletions,
                    "net_lines": total_insertions - total_deletions
                }
            }

            SPRINT(srecord)

            if sync_changes and not last_commit is None:
                changes_table(last_commit, commit, commit.stats.files)

            last_commit = commit

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
        '--no-changes',
        help='flag to indicate if changes table should not be generated',
        action='store_false',
        dest="sync_changes",
        default=True)
    args = parser.parse_args()

    configs = json.load(args.conf)

    for repo_name, conf in configs.items():
        mailmap_path = conf[".mailmap"]
        mailmap = load_mailmap(mailmap_path) if mailmap_path else []
        scan_commits(repo_name, conf, mailmap, args.sync_changes)

if __name__ == "__main__":
    main()
