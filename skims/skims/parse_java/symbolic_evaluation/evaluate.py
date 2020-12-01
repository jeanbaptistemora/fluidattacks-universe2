# Standard library
import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from parse_java.symbolic_evaluation import (
    common,
)
from parse_java.symbolic_evaluation.rules import (
    generic,
)
from utils.logs import (
    blocking_log,
)

# Constants
RECURSIVE = {
    'ADD',
    'BINDING',
    'CALL',
    'CLASS_INSTANTIATION',
}
NON_RECURSIVE = {
    'LITERAL',
    'LOOKUP',
}
ALL_TYPES = NON_RECURSIVE | RECURSIVE

# Typing
Assertion = Dict[str, Dict[str, Any]]
Statement = Dict[str, Any]


def _analyze_context(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
) -> common.Context:
    ctx = common.ensure_context(None)

    # Walk the path and mine the nodes in order to increase the context
    for n_id in path:
        generic.evaluate(graph, n_id, ctx=ctx)

    # Remove temporal state
    ctx.pop('seen')

    return ctx


def _is_linear_or_flatten_one_level(statements: List[Statement]) -> bool:
    finished: bool = True
    statement_index = -1

    for statement in statements.copy():
        statement_index += 1
        statement_type = statement['type']

        # Already linearized this statement
        if '__linear__' in statement:
            continue

        if statement_type in NON_RECURSIVE:
            statement['__linear__'] = True
            statement['stack'] = 0
        elif statement_type in RECURSIVE:
            stack = 0
            for stack_name in {'stack', 'stack_0', 'stack_1'}:
                if stack_name not in statement:
                    continue

                for arg in statement[stack_name]:
                    arg_type = arg['type']

                    if arg_type in ALL_TYPES:
                        statements.insert(statement_index, arg)
                        statement_index += 1
                        stack += 1
                    else:
                        raise NotImplementedError(arg_type)

                    if arg_type in RECURSIVE:
                        finished = False

                statement[stack_name] = -1 * stack
                statement['__linear__'] = True
        else:
            raise NotImplementedError(statement_type)

    return finished


def _linearize_statements(statements: List[Statement]) -> List[Statement]:
    # Linearize one level until it's absolutely flattened
    while not _is_linear_or_flatten_one_level(statements):
        pass

    # Remove temporary meta data
    for statement in statements:
        statement.pop('__linear__', None)

    return statements


def evaluate(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
    *,
    allow_incomplete: bool = False,
) -> Optional[List[Statement]]:
    ctx = _analyze_context(graph, path)

    if ctx['complete'] or allow_incomplete:
        statements = _linearize_statements(ctx['statements'])

        # Debugging information, only visible with skims --debug
        blocking_log('debug', '%s', json.dumps(statements, indent=2))

        return statements

    return None
