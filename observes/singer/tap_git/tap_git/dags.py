#!/usr/bin/env python3
"""Module to analize commit DAGs."""

# everything inside this file is refered to a topological order on the DAG
# don't think about dates, they are irrelevant, think about commit's pointers.

import os
import re
import datetime
import contextlib

from typing import Iterator, List, Any
from collections import OrderedDict

SHA = str


def get_next_match(iterable: Iterator[str], pattern: Any) -> Any:
    """Iterates the iterable until an element matches the pattern."""
    while 1:
        element = next(iterable)
        match = pattern.match(element)
        if match:
            return match.groups()


def get_commits(path: str) -> OrderedDict:  # noqa
    """Return the commits DAG and inverse DAG."""
    # everything will be stored here
    commits: OrderedDict = OrderedDict()

    # get output of command as string
    git_rev_list: str = os.popen((
        f"git -C '{path}'                  "
        f"  rev-list                       "
        f"    --pretty='!%H!!%at!!%ct!!%P!'"
        f"    --graph                      "
        f"    HEAD                         ")).read()

    # parse the git rev-list into commits
    get_commits__parse_git_rev_list(commits, git_rev_list)

    # stamp the integration date
    get_commits__stamp_integration_date(commits)

    # stamp the time it took to reach master
    get_commits__stamp_time_to_master(commits)

    return commits


def get_commits__parse_git_rev_list(
        commits: OrderedDict, git_rev_list: str) -> None:
    """Parses the git rev-list command into the commits datastructure."""
    # create an iterator
    iter_git_rev_list: Iterator[str] = iter(git_rev_list.splitlines())

    # regexp to match the lines of git_rev_list
    rev_list_node = re.compile(
        r"(.*) commit ([0-9a-fA-F]{40})")
    rev_list_info = re.compile(
        r".* !([0-9a-fA-F]{40})!!(.*)!!(.*)!!((?:[0-9a-fA-F]{40} ?)*)!")

    # get base information by parsing git rev-list
    with contextlib.suppress(StopIteration):
        while True:
            # iter until the next node
            graph, commit_node_sha = \
                get_next_match(iter_git_rev_list, rev_list_node)
            # iter until the next info
            commit_info_sha, authored, committed, parents_str =  \
                get_next_match(iter_git_rev_list, rev_list_info)
            # check data integrity
            if not commit_node_sha == commit_info_sha:
                raise Exception(f"Not {commit_node_sha} == {commit_info_sha}.")

            authored = datetime.datetime.utcfromtimestamp(int(authored))
            committed = datetime.datetime.utcfromtimestamp(int(committed))

            parents_list: List[SHA] = \
                [] if not parents_str else parents_str.split(" ")
            parents_count: int = len(parents_list)
            commits[commit_node_sha] = {
                "is_master": graph[0] == "*",
                "is_merge": parents_count >= 2,
                "parents": parents_list,
                "nparents": parents_count,
                "authored_at": authored,
                "committed_at": committed,

                # used when stamping the integration date
                "visit__stamp_integration_date": True,
            }


def get_commits__stamp_integration_date(commits: OrderedDict) -> None:
    """Stamp the integration date into the commits datastructure."""
    follow: List[SHA] = []
    for commit_sha in reversed(commits):
        if commits[commit_sha]["is_master"]:
            commits[commit_sha]["integration_authored_at"] = \
                commits[commit_sha]["authored_at"]
            commits[commit_sha]["integration_committed_at"] = \
                commits[commit_sha]["committed_at"]
            if commits[commit_sha]["is_merge"]:
                get_commits__stamp_integration_date__replace_until_master(
                    commits, commit_sha, follow)
                while follow:
                    parent_sha = follow.pop(0)
                    get_commits__stamp_integration_date__replace_until_master(
                        commits, parent_sha, follow)


def get_commits__stamp_integration_date__replace_until_master(
        commits: OrderedDict, replace_sha: SHA, follow: List[SHA]) -> None:
    """Recursively replace commits traversing DAG but stoping in master."""
    for parent_sha in commits[replace_sha]["parents"]:
        if not commits[parent_sha]["is_master"]:
            if commits[parent_sha]["visit__stamp_integration_date"]:
                commits[parent_sha]["visit__stamp_integration_date"] = \
                    False
                commits[parent_sha]["integration_authored_at"] = \
                    commits[replace_sha]["integration_authored_at"]
                commits[parent_sha]["integration_committed_at"] = \
                    commits[replace_sha]["integration_committed_at"]
                follow.append(parent_sha)


def get_commits__stamp_time_to_master(commits: OrderedDict) -> None:
    """Stamp the time to master as a property of every commit in commits."""
    for commit_sha in commits.keys():
        # graph may contain active branches when cloning without the
        #   --single-branch flag:
        #
        # ...
        # * commit 81c4d4e5
        # |
        # | X commit cbb6d377
        # | |\
        # |/ /
        # | X commit 3676c545
        # |/
        # * commit d75fb8cd
        # ...
        #
        # commits marked as "X" don't have integration date yet:
        #   in a future may be integrated,
        #   in a future may be discarded,
        # there is no way to predict the future
        #   mark them as -1 until confirming they are part of master:
        if "integration_authored_at" in commits[commit_sha] and \
           "integration_committed_at" in commits[commit_sha]:
            commits[commit_sha]["time_to_master_authored"] = (
                commits[commit_sha]["integration_authored_at"]
                - commits[commit_sha]["authored_at"]).total_seconds()
            commits[commit_sha]["time_to_master_committed"] = (
                commits[commit_sha]["integration_committed_at"]
                - commits[commit_sha]["committed_at"]).total_seconds()
        else:
            commits[commit_sha]["time_to_master_authored"] = -1
            commits[commit_sha]["time_to_master_committed"] = -1
