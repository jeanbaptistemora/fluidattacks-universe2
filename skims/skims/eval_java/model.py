# Standard library
from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    List,
    NamedTuple,
    Optional,
    Set,
)


@dataclass
class StatementMeta:
    danger: bool
    linear: bool
    sink: Optional[str]
    stack: int


def get_default_statement_meta() -> StatementMeta:
    return StatementMeta(
        danger=False,
        linear=False,
        sink=None,
        stack=0,
    )


Statement = Any
Statements = List[Statement]


class StatementAdd(NamedTuple):
    stack_0: Statements
    stack_1: Statements
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementAdd'


class StatementBinding(NamedTuple):
    stack: Statements
    var: str
    var_type: str
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementBinding'


class StatementClassInstantiation(NamedTuple):
    class_type: str
    stack: Statements
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementClassInstantiation'


class StatementCustomMethodInvocation(NamedTuple):
    method: str
    stack: Statements
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementCustomMethodInvocation'


class StatementLookup(NamedTuple):
    symbol: str
    meta: StatementMeta

    recursive: bool = False
    type: str = 'StatementLookup'


class StatementLiteral(NamedTuple):
    value: str
    meta: StatementMeta

    recursive: bool = False
    type: str = 'StatementLiteral'


@dataclass
class Context:
    complete: bool
    seen: Set[str]
    statements: Statements


OptionalContext = Optional[Context]
