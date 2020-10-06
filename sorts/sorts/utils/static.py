# Standard libraries
import os
from typing import (
    List,
    Tuple,
)


def read_allowed_names() -> Tuple[List[str], ...]:
    """
    Returns a Tuple containing:
        - A list of allowed extensions to filter repository files
        - A list of allowed configuration files to filter repository files
    """
    allowed_names: List[List[str]] = []
    for name in ['extensions.lst', 'composites.lst']:
        with open(f'{os.path.dirname(__file__)}/../static/{name}') as file:
            content_as_list = file.read().split('\n')
            allowed_names.append(list(filter(None, content_as_list)))
    return (allowed_names[0], allowed_names[1])
