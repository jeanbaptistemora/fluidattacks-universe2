from typing import (
    Any,
    List,
    NamedTuple,
)

# Constants
Attribute = NamedTuple('Attribute', [
    ('column', int),
    ('key', str),
    ('line', int),
    ('val', Any),
])

Block = NamedTuple('Block', [
    ('namespace', List[Any]),
    ('body', List[Any]),
    ('column', int),
    ('line', int),
])

Json = NamedTuple('Json', [
    ('column', int),
    ('data', Any),
    ('line', int),
])
