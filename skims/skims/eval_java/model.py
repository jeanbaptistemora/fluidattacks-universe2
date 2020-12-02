# Standard library
from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypedDict,
)

# Model definition
Statement = Dict[str, Any]
Statements = List[Statement]


class Context(TypedDict):
    complete: bool
    seen: set
    statements: Statements


OptionalContext = Optional[Context]
