# Standard library
import json
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from utils.logs import (
    blocking_log,
)

# Typing
Assertion = Dict[str, Dict[str, Any]]
Statement = Dict[str, Any]


def _read_stack(statements: List[Statement], index: int) -> List[Statement]:
    return statements[index + statements[index]['stack']:index]


def _binding(statements: List[Statement], index: int) -> None:
    statement = statements[index]
    var_type = statement['var_type']

    # Analyze the arguments involved in the assignment
    args = _read_stack(statements, index)
    args_danger = any(arg['__danger__'] for arg in args)

    # Analyze if the binding itself is sensitive
    bind_danger = any((
        # This type is an HTTP request from JavaX framework
        var_type == 'HttpServletRequest',
    ))

    # Local context
    statement['__danger__'] = bind_danger or args_danger


def _literal(statement: Statement) -> None:
    # A literal is constant, no danger there
    statement['__danger__'] = False


def _call(statements: List[Statement], index: int) -> None:
    statement = statements[index]

    # Analyze if the arguments involved in the function are dangerous
    args = _read_stack(statements, index)
    args_danger = any(arg['__danger__'] for arg in args)

    # Analyze if the call itself is sensitive
    method = statement['method']
    call_danger = any((
        method.endswith('.getCookies'),
    ))

    # Local context
    statement['__danger__'] = args_danger or call_danger


def get(statements: List[Statement]) -> List[Statement]:
    for index, statement in enumerate(statements):
        statement['__danger__'] = None
        statement_type = statement['type']

        if statement_type == 'ADD':
            pass
        elif statement_type == 'BINDING':
            _binding(statements, index)
        elif statement_type == 'CALL':
            _call(statements, index)
        elif statement_type == 'CLASS_INSTANTIATION':
            pass
        elif statement_type == 'LITERAL':
            _literal(statement)
        elif statement_type == 'LOOKUP':
            pass
        else:
            raise NotImplementedError(statement_type)

    # Debugging information, only visible with skims --debug
    blocking_log('debug', '%s', json.dumps(statements, indent=2))

    return statements
