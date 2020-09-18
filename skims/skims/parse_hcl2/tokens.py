from typing import (
    Any,
    NamedTuple,
)

# Constants
Attribute = NamedTuple('Attribute', [
    ('key', str),
    ('val', Any),
])
