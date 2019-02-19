"""Metrics module."""

import os
import re
import sys
import time
import json
import asyncio
import statistics

from typing import List, Dict, Any

# pylint: disable=relative-beyond-top-level
from . import os_tools


def scan_metrics(repository: str, path: str) -> None:
    """Dispatcher and manager."""
    os.chdir(path)
    # command to get non-bynary files in HEAD
    git_trick = (
        # grep lines that are in file 2 and not in file 1
        "grep -Fvxf"
        #    file 1: all binary files
        "    <(grep -Fvxf"
        #        file 1: list non-binary files in git history
        "        <(git grep -Il '')"
        #        file 2: list all files in git history
        "        <(git grep -al '')"
        "    )"
        #    file 2: all files in HEAD
        "    <(git ls-tree --name-only -r HEAD)")

    # list of paths to non-bynary files in HEAD
    file_paths: List[str] = os_tools.get_stdout_stderr(
        ["bash", "-c", git_trick])[0].splitlines()

    # Dict[file_path, List[blame_entry]]
    blames: Dict[str, List[Dict[str, Any]]] = get_blames(file_paths)

    write_schemas()
    write_records__lines_per_actor(repository, blames)
    write_records__median_line_times_per_autor(repository, blames)


def get_blames(file_paths: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """Get blames asynchronously."""
    schunk = len(file_paths) // 4
    file_paths_1 = file_paths[0: 1 * schunk]
    file_paths_2 = file_paths[1 * schunk: 2 * schunk]
    file_paths_3 = file_paths[2 * schunk: 3 * schunk]
    file_paths_4 = file_paths[3 * schunk:]

    tasks = [
        get_async_blames(file_paths_1),
        get_async_blames(file_paths_2),
        get_async_blames(file_paths_3),
        get_async_blames(file_paths_4),
    ]

    loop = asyncio.get_event_loop()
    blames_sublist = loop.run_until_complete(asyncio.gather(*tasks))
    blames = {
        **blames_sublist[0],
        **blames_sublist[1],
        **blames_sublist[2],
        **blames_sublist[3]
    }
    return blames


async def get_async_blames(
        file_paths: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """Return a Dict[file_path] = List(blame_entry)."""
    blames: Dict[str, List[Dict[str, Any]]] = {}
    for file_path in file_paths:
        blames[file_path] = []

        git_trick = (
            f'git blame --line-porcelain HEAD "{file_path}"'
            f'  | grep -E'
            f'    "^([0-9a-f]{40}|author|author-mail|author-time|filename) "')

        raw_blame = os_tools.get_stdout_stderr(
            ["bash", "-c", git_trick])[0]

        blame_entry: Dict[str, Any] = {}
        for line in raw_blame.splitlines():
            tokens = line.split(" ", 1)
            if re.match(r"[0-9a-f]{40}", tokens[0]):
                blame_entry = {}
            elif tokens[0] in ("author", "author-mail",):
                blame_entry[tokens[0]] = tokens[1]
            elif tokens[0] == "author-time":
                try:
                    blame_entry["author-time"] = float(tokens[1])
                except ValueError:
                    pass
            elif tokens[0] == "filename":
                safety_checks = (
                    "author" in blame_entry,
                    "author-mail" in blame_entry,
                    "author-time" in blame_entry,
                )
                if all(safety_checks):
                    blames[file_path].append(blame_entry)
                else:
                    print(
                        f"WARN: Exception at: {file_path} {str(blame_entry)}",
                        file=sys.stderr, flush=True)

    return blames


def get_lines_per_actor(
        blames: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
    """Return the number of lines per actor in HEAD."""
    lines_per_actor: Dict[str, int] = {}
    for _, blame_entries in blames.items():
        for blame_entry in blame_entries:
            author_name = blame_entry["author"]
            author_email = blame_entry["author-mail"]
            actor_id = f"{author_name} {author_email}"
            try:
                lines_per_actor[actor_id] += 1
            except KeyError:
                lines_per_actor[actor_id] = 1
    return lines_per_actor


def get_median_line_times_per_autor(
        blames: Dict[str, List[Dict[str, Any]]]) -> Dict[str, float]:
    """Return the median time a line have been in HEAD."""

    line_times: Dict[str, List[float]] = {}
    for _, blame_entries in blames.items():
        for blame_entry in blame_entries:
            author_name = blame_entry["author"]
            author_email = blame_entry["author-mail"]
            author_time = blame_entry["author-time"]
            actor_id = f"{author_name} {author_email}"
            try:
                line_times[actor_id].append(time.time() - author_time)
            except KeyError:
                line_times[actor_id] = [time.time() - author_time]

    seconds_per_month = 60.0 * 60.0 * 24.0 * 30.0
    median_line_times_per_autor = {
        actor: statistics.median(line_times_actor) / seconds_per_month
        for actor, line_times_actor in line_times.items()
    }
    return median_line_times_per_autor


def write_schemas() -> None:
    """Write schemas to stdout."""
    schemas = (
        "metrics_lines_per_actor.schema.json",
        "metrics_median_line_age.schema.json",
    )
    for schema in schemas:
        with open(f"{os.path.dirname(__file__)}/{schema}", "r") as file:
            print(json.dumps(json.load(file)))


def write_records__lines_per_actor(
        repository: str,
        blames: Dict[str, List[Dict[str, Any]]]) -> None:
    """Write records to stdout."""
    records: Dict[str, int] = get_lines_per_actor(blames)
    for actor_id, lines in records.items():
        srecord = {
            "type": "RECORD",
            "stream": "metrics_lines_per_actor",
            "record": {
                "repository": repository,
                "actor_id": actor_id,
                "lines": lines,
            }
        }
        print(json.dumps(srecord))


def write_records__median_line_times_per_autor(
        repository: str,
        blames: Dict[str, List[Dict[str, Any]]]) -> None:
    """Write records to stdout."""
    records: Dict[str, float] = get_median_line_times_per_autor(blames)
    for actor_id, median_line_age in records.items():
        srecord = {
            "type": "RECORD",
            "stream": "metrics_median_line_age",
            "record": {
                "repository": repository,
                "actor_id": actor_id,
                "median_line_age": median_line_age,
            }
        }
        print(json.dumps(srecord))
