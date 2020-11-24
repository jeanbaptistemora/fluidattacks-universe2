# Standard library
from typing import (
    Any,
    Dict,
)


def is_positional_node(node: Dict[str, Any]) -> bool:
    keys = set(node.keys())

    return keys == {'c', 'l', 'text', 'type'}
