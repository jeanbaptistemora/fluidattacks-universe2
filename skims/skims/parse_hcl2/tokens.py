from typing import (
    Any,
    NamedTuple,
)

# Constants
Attribute = NamedTuple(
    "Attribute",
    [
        ("column", int),
        ("key", str),
        ("line", int),
        ("val", Any),
    ],
)

Block = NamedTuple(
    "Block",
    [
        ("namespace", list[Any]),
        ("body", list[Any]),
        ("column", int),
        ("line", int),
    ],
)

Json = NamedTuple(
    "Json",
    [
        ("column", int),
        ("data", Any),
        ("line", int),
    ],
)
