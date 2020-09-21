from typing import (
    Any,
    List,
    NamedTuple,
)

# Constants
Attribute = NamedTuple('Attribute', [
    ('key', str),
    ('val', Any),
])

Block = NamedTuple('Block', [
    ('namespace', List[Any]),
    ('body', List[Any]),
])
