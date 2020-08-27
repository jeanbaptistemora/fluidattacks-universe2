# Standard library
import contextlib
import functools
import os
import re
import tempfile
import textwrap
from itertools import filterfalse
from operator import methodcaller
from typing import (
    Generator,
    Iterator,
    Pattern,
    Tuple,
)


@functools.lru_cache(maxsize=None, typed=True)
def _compile(regexps: Tuple[str, ...]) -> Tuple[Pattern, ...]:
    return tuple(map(re.compile, regexps))


def _iter_full_paths(path: str) -> Iterator[str]:
    """Recursively yield full paths to files for a given starting path."""
    if os.path.isfile(path):
        yield path
    elif os.path.exists(path):
        for entry in os.scandir(path):
            full_path = entry.path
            if entry.is_dir(follow_symlinks=False):
                yield from _iter_full_paths(full_path)
            else:
                yield full_path


def _iter_rel_paths(starting_path: str) -> Iterator[str]:
    """Recursively yield relative paths to files for a given starting path."""
    yield from (
        path.replace(starting_path, '')[1:]
        for path in _iter_full_paths(starting_path)
    )


@contextlib.contextmanager
def create_ephemeral(
    suffix: str,
    content: str,
) -> Generator[str, None, None]:
    """Creates a tempfile.NamedTemporaryFile and yields its name."""
    content = content[1:]
    content = textwrap.dedent(content)
    with tempfile.NamedTemporaryFile(suffix=suffix) as file:
        file.write(content.encode())
        file.seek(0)

        yield file.name


def is_covered(
    *,
    path: str,
    include_regexps: Tuple[str, ...],
    exclude_regexps: Tuple[str, ...],
) -> bool:
    """Return True if a file should be included according to the filters."""
    is_included_in_any_rule: bool = \
        any(map(methodcaller('match', path), _compile(include_regexps)))
    is_excluded_in_any_rule: bool = \
        any(map(methodcaller('match', path), _compile(exclude_regexps)))

    return \
        not is_excluded_in_any_rule \
        and is_included_in_any_rule


def iter_non_matching_files(
    *,
    path: str,
    include_regexps: Tuple[str, ...],
    exclude_regexps: Tuple[str, ...],
) -> Iterator[str]:
    """Yield non-matching paths for the include/exclude regular expresions.

    Include/exclude regular expresions are considered relative.
    This means that regular expresions will be matched against the string
    that is after 'path/'
    """
    def predicate(file: str) -> bool:
        return is_covered(
            path=file,
            include_regexps=include_regexps,
            exclude_regexps=exclude_regexps,
        )

    yield from filterfalse(predicate, _iter_rel_paths(path))
