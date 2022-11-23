# -*- coding: utf-8 -*-

"""Asserts generic meta-method."""


import asyncio
from fluidasserts import (
    CLOSED,
    LOW,
    method_stats_set_owner,
    OPEN,
    Result,
    Unit,
    UNKNOWN,
)
from fluidasserts.helper import (
    asynchronous,
)
from fluidasserts.utils.decorators import (
    api,
    mp_track,
    unknown_if,
)
from functools import (
    lru_cache,
)
import hashlib
import os
import oyaml as yaml
import sys
from typing import (
    Callable,
    List,
    Union,
)


def _scan_for_files(path: str):
    """Recursively yield full paths to files for a given directory."""
    if os.path.isfile(path):
        yield path
    else:
        for entry in os.scandir(path):
            full_path = entry.path
            if entry.is_dir(follow_symlinks=False):
                yield from _scan_for_files(full_path)
            else:
                yield full_path


def _scan_for_dirs(path: str):
    """Recursively yield full paths to dirs for a given directory."""
    if os.path.isdir(path):
        yield path
        for entry in os.scandir(path):
            full_path = entry.path
            if entry.is_dir(follow_symlinks=False):
                yield full_path
                yield from _scan_for_dirs(full_path)


@lru_cache(maxsize=None, typed=True)
def _full_paths_in_path(path: str) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    return tuple(_scan_for_files(path))


# pylint: disable=unused-argument
@api(risk=LOW, kind="Generic")
@unknown_if(Exception)
def check_function(func: Callable, *args, metadata=None, **kwargs) -> bool:
    """Run arbitrary code and return results in Asserts format.

    This is useful for verifying very specific scenarios.

    :param func: Callable function that will return True if the
    vulnerability is found open or False (or any Python null value) if found
    closed.
    :param *args: Positional parameters that will be passed to func.
    :param *kwargs: Keyword parameters that will be passed to func.
    """
    if asyncio.iscoroutinefunction(func):
        ret = asynchronous.run_func(
            func, ((args, kwargs),), return_exceptions=False
        )[0]
    else:
        ret = func(*args, **kwargs)

    is_check_open: bool = bool(ret)
    msg_open: str = "Check was found open"
    msg_closed: str = "Check was found closed"

    unit = Unit(
        where="Custom function call",
        specific=[msg_open if is_check_open else msg_closed],
    )

    if is_check_open:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


@lru_cache(maxsize=None, typed=True)
def get_paths(
    path: str, exclude: tuple = tuple(), endswith: tuple = tuple()
) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    paths = _full_paths_in_path(path)
    if exclude:
        paths = filter(lambda p: not any(e in p for e in exclude), paths)
    if endswith:
        paths = filter(lambda p: any(p.endswith(e) for e in endswith), paths)
    return tuple(paths)


def get_paths_tree(
    path: str, exclude: tuple = tuple(), endswith: tuple = tuple()
):
    """Return a directory tree."""
    paths = []
    for root, dirs, files in os.walk(path):
        if exclude:
            files = [
                file
                for file in files
                if not any(e in f"{root}/{file}" for e in exclude)
            ]
        if endswith:
            files = [
                file
                for file in files
                if any(f"{root}/{file}".endswith(e) for e in endswith)
            ]
        paths.append((root, dirs, files))
    return paths


@lru_cache(maxsize=None, typed=True)
def get_dir_paths(path: str, exclude: tuple = tuple()) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    paths = _scan_for_dirs(path)
    if exclude:
        paths = filter(lambda p: not any(e in p for e in exclude), paths)
    return tuple(paths)


@lru_cache(maxsize=None, typed=True)
def get_sha256(path: str) -> str:
    """
    Get SHA256 digest of a file or a directory.

    :param path: Path to the file to digest.
    """
    sha256 = hashlib.sha256()
    if path is not None and os.path.exists(path):
        for fpath in get_paths(path):
            with open(fpath, "rb", buffering=0) as handle:
                block = handle.read(128 * 1024)
                while block:
                    sha256.update(block)
                    block = handle.read(128 * 1024)
    return sha256.hexdigest()


def add_finding(finding: str) -> bool:
    """Print finding as part of the Asserts output.

    :param finding: Current project context.
    """
    method_stats_set_owner(finding)
    message = yaml.safe_dump(
        {"finding": finding},
        default_flow_style=False,
        explicit_start=True,
        allow_unicode=True,
    )
    print(message, end="", flush=True, file=sys.stdout)
    print(message, end="", flush=True, file=sys.stderr)
    return True


class FluidAsserts:
    """
    Generic context manager to assert security assumptions.

    :examples:

        - ``Static Application Security Testing (SAST) check``

          .. literalinclude:: example/creator-sast.exp
              :linenos:
              :language: python

          Once you run your exploit with Asserts you'll get:

          .. literalinclude:: example/creator-sast.exp.out
              :language: yaml
              :lines: 15-28

        - ``Dynamic Application Security Testing (DAST) check``

          .. literalinclude:: example/creator-dast.exp
              :linenos:
              :language: python

          Once you run your exploit with Asserts you'll get:

          .. literalinclude:: example/creator-dast.exp.out
              :language: yaml
              :lines: 15-28

        - Errors inside the exploit automatically mark the check
          as ``UNKNOWN``:

          .. literalinclude:: example/creator-errors.exp
              :linenos:
              :language: python

          Once you run your exploit with Asserts you'll get:

          .. literalinclude:: example/creator-errors.exp.out
              :language: yaml
              :lines: 15-22

        Just in case you need it,
        the resultant :class:`fluidasserts.Result` object can be accessed at::

            creator.result
    """

    __name__ = "FluidAsserts"

    def __init__(self, *, risk: str, kind: str, message: str):
        """Initialize the parameters for the context manager."""
        self._message: str = message
        self._open_units: List[Unit] = []
        self._closed_units: List[Unit] = []

        self.result = Result(
            risk=risk,
            kind=kind,
            func=self,
            func_args=[],
            func_kwargs={"risk": risk, "kind": kind, "message": message},
        )

        # Notify that the check is running
        print(f"  check: {self.result.func_id}", file=sys.stderr, flush=True)

        # Track the function
        mp_track(self.result.func_id)

    def __enter__(self):
        """What we are going to do once it gets called from the with block."""
        return self

    def set_open(self, *, where: str, specific: List[Union[int, str]]):
        """
        Add a cardinality with status ``OPEN``.

        :param where: Location of the cardinality, a path for Static (SAST)
                      checks, a url or host:port for Dynamic (DAST)
                      checks.
        :param specific: The vulnerable line for SAST Checks or the input field
                         for dynamic checks.
        """
        self._open_units.append(Unit(where=where, specific=specific))

    def set_closed(self, *, where: str, specific: List[Union[int, str]]):
        """
        Add a cardinality with status ``CLOSED``.

        :param where: Location of the cardinality, a path for Static (SAST)
                      checks, a url or host:port for Dynamic (DAST)
                      checks.
        :param specific: The vulnerable line for SAST Checks or the input field
                         for dynamic checks.
        """
        self._closed_units.append(Unit(where=where, specific=specific))

    def __exit__(self, exc_type, exc_value, _) -> bool:
        """Handle exceptions and print results."""
        if exc_type:
            status: str = UNKNOWN
            message: str = f"An error occurred: {exc_value}"
        else:
            status = OPEN if self._open_units else CLOSED
            message = self._message

        # Append the results to the Result object
        self.result.set_status(status)
        self.result.set_message(message)
        self.result.set_vulns(self._open_units)
        self.result.set_safes(self._closed_units)

        # Register it to the stats
        self.result.register_stats()

        # Print
        self.result.print()

        # If exceptions happened inside the block:
        #   They will not propagate
        #   The check will be marked as UNKNOWN
        return True

    __wrapped__ = __init__
