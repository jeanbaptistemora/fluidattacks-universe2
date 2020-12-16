# Standard library
from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
)


class StopEvaluation(Exception):
    pass


@dataclass
class StatementMeta:
    danger: bool
    linear: bool
    sink: Optional[str]
    stack: int
    value: Optional[Any]


def get_default_statement_meta() -> StatementMeta:
    return StatementMeta(
        danger=False,
        linear=False,
        sink=None,
        stack=0,
        value=None,
    )


Statement = Any
Statements = List[Statement]


class ExpressionConditional(NamedTuple):
    meta: StatementMeta
    stacks: List[Statements]

    recursive: bool = True
    type: str = 'ExpressionConditional'


class ExpressionRelational(NamedTuple):
    meta: StatementMeta
    operator: str
    stacks: List[Statements]

    recursive: bool = True
    type: str = 'ExpressionRelational'


class ExpressionUnary(NamedTuple):
    meta: StatementMeta
    operator: str
    stack: Statements

    recursive: bool = True
    type: str = 'ExpressionUnary'


class ExpressionBinary(NamedTuple):
    meta: StatementMeta
    operator: str
    stacks: List[Statements]

    recursive: bool = True
    type: str = 'ExpressionBinary'


class StatementAdd(NamedTuple):
    meta: StatementMeta
    sign: str
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


class StatementCustomMethodInvocationChain(NamedTuple):
    meta: StatementMeta
    method: str
    stacks: List[Statements]

    recursive: bool = True
    type: str = 'StatementCustomMethodInvocationChain'


class StatementDeclaration(NamedTuple):
    stack: Statements
    var: str
    var_type: str
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementDeclaration'


class StatementIf(NamedTuple):
    cfg_condition: str
    stack: Statements
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementIf'


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


class StatementPass(NamedTuple):
    meta: StatementMeta

    recursive: bool = False
    type: str = 'StatementPass'


class StatementPrimary(NamedTuple):
    stacks: List[Statements]
    meta: StatementMeta

    recursive: bool = True
    type: str = 'StatementPrimary'


@dataclass
class Context:
    complete: bool
    path_edges: Dict[str, str]
    seen: Set[str]
    statements: Statements


OptionalContext = Optional[Context]
