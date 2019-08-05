#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""Asserts generic meta-method."""

# standard imports
import os
import sys
import asyncio
import hashlib
from functools import lru_cache

# 3rd party imports
import yaml
from typing import Callable

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts import method_stats_set_owner
from fluidasserts.helper import asynchronous
from fluidasserts.utils.decorators import track, level, notify

# pylint: disable=broad-except


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
    return


@lru_cache(maxsize=None, typed=True)
def _full_paths_in_path(path: str) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    return tuple(_scan_for_files(path))


@notify
@level('low')
@track
def check_function(func: Callable, *args, **kwargs) -> bool:
    """Run arbitrary code and return results in Asserts format.

    This is useful for verifying very specific scenarios.

    :param func: Callable function that will return True if the
    vulnerability is found open or False (or any Python null value) if found
    closed.
    :param *args: Positional parameters that will be passed to func.
    :param *kwargs: Keyword parameters that will be passed to func.
    """
    metadata = kwargs.pop('metadata', None)
    try:
        if asyncio.iscoroutinefunction(func):
            ret = asynchronous.run_func(
                func, ((args, kwargs),), return_exceptions=False)[0]
        else:
            ret = func(*args, **kwargs)
    except Exception as exc:
        show_unknown('Function returned an error',
                     details=dict(metadata=metadata,
                                  function_call=dict(args=args,
                                                     kwargs=kwargs),
                                  error=repr(exc).replace(':', ',')))
    else:
        if ret:
            show_open('Function check was found open',
                      details=dict(metadata=metadata,
                                   function_call=dict(args=args,
                                                      kwargs=kwargs,
                                                      return_value=ret)))
            return True
        else:
            show_close('Function check was found closed',
                       details=dict(metadata=metadata,
                                    function_call=dict(args=args,
                                                       kwargs=kwargs,
                                                       return_value=ret)))
    return False


@lru_cache(maxsize=None, typed=True)
def get_paths(path: str,
              exclude: tuple = tuple(),
              endswith: tuple = tuple()) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    paths = _full_paths_in_path(path)
    if exclude:
        paths = filter(lambda p: not any(e in p for e in exclude), paths)
    if endswith:
        paths = filter(lambda p: any(p.endswith(e) for e in endswith), paths)
    return tuple(paths)


@lru_cache(maxsize=None, typed=True)
def get_dir_paths(path: str,
                  exclude: tuple = tuple()) -> tuple:
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
        for path in get_paths(path):
            with open(path, 'rb', buffering=0) as handle:
                for block in iter(lambda: handle.read(128 * 1024), b''):
                    sha256.update(block)
    return sha256.hexdigest()


def add_finding(finding: str) -> bool:
    """Print finding as part of the Asserts output.

    :param finding: Current project context.
    """
    method_stats_set_owner(finding)
    message = yaml.safe_dump({'finding': finding},
                             default_flow_style=False,
                             explicit_start=True,
                             allow_unicode=True)
    print(message, end='', flush=True, file=sys.stdout)
    print(message, end='', flush=True, file=sys.stderr)
    return True
