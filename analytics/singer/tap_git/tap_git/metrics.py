"""Metrics module."""

import os
import time
import json
import asyncio
import subprocess
import statistics

from typing import Tuple, List, Dict


def get_output(command: List[str]) -> Tuple[str, str]:
    """Return the stdout and stderr of a command."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    raw_stdout, raw_stderr = process.communicate()
    stdout = "" if raw_stdout is None else raw_stdout.decode(
        "utf-8", "backslashreplace")
    stderr = "" if raw_stderr is None else raw_stderr.decode(
        "utf-8", "backslashreplace")
    return stdout, stderr


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
    file_paths: List[str] = get_output(
        ["bash", "-c", git_trick])[0].splitlines()

    # Dict[file_path, List[blame_entry]]
    blames: Dict[str, List[Dict[str, str]]] = get_blames(file_paths)

    write_schemas()
    write_records__lines_per_actor(repository, blames)
    write_records__median_line_times_per_autor(repository, blames)


def get_blames(file_paths: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """."""
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
        file_paths: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Return a Dict[file_path] = List(blame_entry)."""
    blames: Dict[str, List[Dict[str, str]]] = {}
    for file_path in file_paths:
        blames[file_path] = []
        git_trick = (
            f"git blame --line-porcelain HEAD \"{file_path}\""
            f" | grep -E \"(author|author-mail|author-time) \"")

        raw_blame = get_output(
            ["bash", "-c", git_trick])[0]

        count = 0
        blame_entry: Dict[str, str] = {}
        for line in raw_blame.splitlines():
            count += 1
            tokens = line.split(" ", 1)
            if count == 1:
                blame_entry = {}
                blame_entry["author"] = tokens[1]
            elif count == 2:
                blame_entry["author-mail"] = tokens[1]
            elif count == 3:
                blame_entry["author-time"] = tokens[1]
                blames[file_path].append(blame_entry)
                count = 0

    return blames


def get_lines_per_actor(
        blames: Dict[str, List[Dict[str, str]]]) -> Dict[str, int]:
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
        blames: Dict[str, List[Dict[str, str]]]) -> Dict[str, float]:
    """Return the median time a line have been in HEAD."""

    line_times: Dict[str, List[float]] = {}
    for _, blame_entries in blames.items():
        for blame_entry in blame_entries:
            author_name = blame_entry["author"]
            author_email = blame_entry["author-mail"]
            author_time = blame_entry["author-time"]
            actor_id = f"{author_name} {author_email}"
            try:
                line_times[actor_id].append(time.time() - float(author_time))
            except KeyError:
                line_times[actor_id] = [time.time() - float(author_time)]

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
        blames: Dict[str, List[Dict[str, str]]]) -> None:
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
        blames: Dict[str, List[Dict[str, str]]]) -> None:
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
