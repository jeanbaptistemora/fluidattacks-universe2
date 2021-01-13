# Standard library
from typing import (
    Set,
)


def build_attr_paths(*attrs: str) -> Set[str]:
    return set('.'.join(attrs[index:]) for index, _ in enumerate(attrs))
