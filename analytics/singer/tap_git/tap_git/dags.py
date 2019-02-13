#!/usr/bin/env python3
"""Module to analize commit DAGs."""

# everything inside this file is refered to a topological order on the DAG
# don't think about dates, they are irrelevant, but commit's pointers.

import os
import re
import datetime

from collections import OrderedDict


def get_next_match(iterable, pattern):
    """Iterates the iterable until an element matches the pattern."""
    while 1:
        element = next(iterable)
        match = pattern.match(element)
        if match:
            return match.groups()


def get_commits(path: str) -> OrderedDict:
    """Return the commits DAG and inverse DAG."""
    commits: OrderedDict = OrderedDict()
    iter_rev_list = iter(os.popen((
        f"cd '{path}';                   "
        f"git rev-list                   "
        f"  --pretty='!%H!!%at!!%ct!!%P!'"
        f"  --graph                      "
        f"  --all                        ")).read().splitlines())

    # regexps to match the output of the magic command
    rev_list_info = re.compile(
        r"[\|\\/_ ]*!([0-9a-fA-F]{40})!!(.*)!!(.*)!!((?:[0-9a-fA-F]{40} ?)*)!")
    rev_list_node = re.compile(
        r"([\|\\/_ \*]*) commit ([0-9a-fA-F]{40})")

    try:
        while 1:
            # iter until the next node
            graph, commit_node_sha = \
                get_next_match(iter_rev_list, rev_list_node)
            # iter until the next info
            commit_info_sha, authored, commited, parents_str =  \
                get_next_match(iter_rev_list, rev_list_info)
            # check data integrity
            if not commit_node_sha == commit_info_sha:
                raise Exception(f"Not {commit_node_sha} == {commit_info_sha}.")

            authored = datetime.datetime.utcfromtimestamp(
                int(authored)).strftime("%Y-%m-%dT%H:%M:%SZ")
            commited = datetime.datetime.utcfromtimestamp(
                int(commited)).strftime("%Y-%m-%dT%H:%M:%SZ")

            parents_list = [] if not parents_str else parents_str.split(" ")
            parents_count = len(parents_list)
            commits[commit_node_sha] = {
                "is_master": graph[0] == "*",
                "is_merge": parents_count >= 2,
                "parents": parents_list,
                "nparents": parents_count,
                "childs": [],
                "nchilds": 0,
                "metadata": {
                    "authored": authored,
                    "commited": commited,
                },
            }
    except StopIteration:
        pass

    for commit_sha in commits.keys():
        for parent_sha in commits[commit_sha]["parents"]:
            commits[parent_sha]["childs"].append(commit_sha)
            commits[parent_sha]["nchilds"] += 1
    for commit_sha in commits.keys():
        commits[commit_sha]["is_fork"] = commits[commit_sha]["nchilds"] >= 2

    return commits


def get_commits_with_adjusted_dates(path: str) -> OrderedDict:
    """Return a datastructure {commit_sha: integration_date}."""
    # get a datastructure {commit_sha : metadata}
    commits = get_commits(path)
    # stamp the integration dates
    for commit_sha in commits.keys():
        commit_is_in_master = commits[commit_sha]["is_master"]
        commit_is_merge_commit = commits[commit_sha]["is_merge"]
        if commit_is_in_master and commit_is_merge_commit:
            get_commits_with_adjusted_dates__replace_until_master(
                commits, commit_sha)
    return commits


def get_commits_with_adjusted_dates__replace_until_master(
        commits, replace_sha: str) -> None:
    """Recursively replace commits traversing DAG but stoping in master."""
    follow = []
    metadata = commits[replace_sha]["metadata"]
    for parent_sha in commits[replace_sha]["parents"]:
        if not commits[parent_sha]["is_master"]:
            commits[parent_sha]["metadata"] = metadata
            follow.append(parent_sha)
    for parent_sha in follow:
        get_commits_with_adjusted_dates__replace_until_master(
            commits, parent_sha)


# def stamp_time_to_master():
#     """Stamp the time to master as a property of every commit in commits."""
    # every commit between a master's fork and a master's merge
    # that is not a master's commit is a commit on the developer hands
    # it est, a commit that's not added value yet, therefore the time between
    # the commit and the merge is the time to market of that commit
    # time to market:
    #   (time of merge commit - min(
    #       time of commit
    #       for commits in all paths from merge_commit to any_node_in_master)))
