"""Metrics module."""

import os
import re
import time
import json
import subprocess
import statistics

from typing import Tuple, List, Dict, Any


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

    # list of paths to files in HEAD
    file_paths: List[str] = get_output(
        ["git", "ls-tree", "--name-only", "-r", "HEAD"])[0].split("\n")

    # Dict[file_path, List[blame_entry]]
    blames: Dict[str, List[Dict[str, str]]] = get_blames(file_paths)

    # compute needed things
    lines_per_actor: Dict[str, int] = get_lines_per_actor(blames)

    median_line_times_per_autor: Dict[str, float] = \
        get_median_line_times_per_autor(blames)

    write_schemas()
    write_records__lines_per_actor(
        repository,
        lines_per_actor)
    write_records__median_line_times_per_autor(
        repository,
        median_line_times_per_autor)


def get_blames(file_paths: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Return a Dict[file_path] = List(blame_entry)."""
    blames: Dict[str, List[Dict[str, str]]] = {}
    for file_path in file_paths:
        blames[file_path] = []
        raw_blame, _ = get_output(
            ["git", "blame", "--line-porcelain", "HEAD", file_path])

        blame_entry: Dict[str, str] = {}
        for line in raw_blame.splitlines():
            if re.match(r"[0-9a-f]{40}", line):
                if blame_entry:
                    blames[file_path].append(blame_entry)
                    blame_entry = {}
                blame_entry["sha1"] = line.split()[0]
            elif re.match(r"^author ", line):
                blame_entry["author"] = " ".join(line.split()[1:])
            elif re.match(r"^author-mail ", line):
                blame_entry["author-mail"] = " ".join(line.split()[1:])
            elif re.match(r"^author-time ", line):
                blame_entry["author-time"] = " ".join(line.split()[1:])
            elif re.match(r"^author-tz ", line):
                blame_entry["author-tz"] = " ".join(line.split()[1:])
        if blame_entry:
            blames[file_path].append(blame_entry)

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
        records: Dict[str, Any]) -> None:
    """Write records to stdout."""
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
        records: Dict[str, Any]) -> None:
    """Write records to stdout."""
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
