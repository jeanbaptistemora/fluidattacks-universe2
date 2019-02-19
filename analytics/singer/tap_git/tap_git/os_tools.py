#!/usr/bin/env python3
"""Module to do some wrappings around command executions."""

import subprocess
from typing import List, Tuple


def get_stdout_stderr(command: List[str]) -> Tuple[str, str]:
    """Return the stdout and stderr of a command utf-8 safely."""
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
