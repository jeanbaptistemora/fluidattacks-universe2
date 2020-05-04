# Standard library
import contextlib
import os
import re
import tempfile
import textwrap
from operator import methodcaller
from typing import (
    Generator,
    Iterator,
    Tuple,
)


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


def iter_matching_files(
    *,
    path: str,
    include_regexps: Tuple[str, ...],
    exclude_regexps: Tuple[str, ...],
) -> Iterator[str]:
    """Yield paths matching the include/exclude regular expresions.

    Include/exclude regular expresions are considered relative.
    This means that regular expresions will be matched against the string
    that is after 'path/'
    """
    include_c_regexps = tuple(
        re.compile(include_regex)
        for include_regex in include_regexps
    )
    exclude_c_regexps = tuple(
        re.compile(exclude_regex)
        for exclude_regex in exclude_regexps
    )

    yield from (
        path
        for path in _iter_rel_paths(path)
        if (
            any(map(methodcaller('match', path), include_c_regexps))
            and not any(map(methodcaller('match', path), exclude_c_regexps))
        )
    )
