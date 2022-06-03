import os
from typing import (
    Any,
    Iterator,
    List,
)


def _flatten(elements: List[str], aux_list: Any = None) -> List[str]:
    aux_list = aux_list if aux_list is not None else []
    for i in elements:
        if isinstance(i, list):
            _flatten(i, aux_list)
        else:
            aux_list.append(i)
    return aux_list


def _scan_for_files(path: str) -> Iterator[str]:
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


def _full_paths_in_path(path: str) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    return tuple(_scan_for_files(path))


def _get_paths(
    path: str, exclude: tuple = tuple(), endswith: tuple = tuple()
) -> tuple:
    """Return a tuple of full paths to files recursively from path."""
    paths = _full_paths_in_path(path)
    if exclude:
        paths = tuple(
            filter(lambda p: not any(e in p for e in exclude), paths)
        )
    if endswith:
        paths = tuple(
            filter(lambda p: any(p.endswith(e) for e in endswith), paths)
        )
    return paths


def _is_primitive(object_: Any) -> bool:
    """Check if an object is of primitive type."""
    return not hasattr(object_, "__dict__")
