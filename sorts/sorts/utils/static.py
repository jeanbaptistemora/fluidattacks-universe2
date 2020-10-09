# Standard libraries
import os
from typing import (
    List,
    Tuple,
)


def read_allowed_names() -> Tuple[List[str], ...]:
    """Reads static lists containing allowed names and extensions"""
    allowed_names: List[List[str]] = []
    for name in ['extensions.lst', 'composites.lst']:
        with open(f'{os.path.dirname(__file__)}/../static/{name}') as file:
            content_as_list = file.read().split('\n')
            allowed_names.append(list(filter(None, content_as_list)))
    return (allowed_names[0], allowed_names[1])
