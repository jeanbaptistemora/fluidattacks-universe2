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
    meta: StatementMeta
    stacks: List[Statements]

    recursive: bool = True
    type: str = 'StatementAdd'


class StatementAssignment(NamedTuple):
    stack: Statements
    var: str
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementAssignment'


class StatementCast(NamedTuple):
    class_type: str
    stack: Statements
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementCast'


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


class StatementDeclaration(NamedTuple):
    stack: Statements
    var: str
    var_type: str
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementDeclaration'


class StatementLookup(NamedTuple):
    symbol: str
    meta: StatementMeta

    recursive: bool = False
    type: str = 'StatementLookup'


class StatementLiteral(NamedTuple):
    value: str
    value_type: str
    meta: StatementMeta

    recursive: bool = False
    type: str = 'StatementLiteral'


class StatementPrimary(NamedTuple):
    stacks: List[Statements]
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementPrimary'


@dataclass
class Context:
    complete: bool
    seen: Set[str]
    statements: Statements


OptionalContext = Optional[Context]
