# Standard library
from typing import (
    Any,
    Dict,
    List,
)

# Typing
Assertion = Dict[str, Dict[str, Any]]
Statement = Dict[str, Any]


def _binding_java_servlet_request(
    assertions: Assertion,
    statement: Statement,
) -> None:
    if all((
        statement['var'] == 'request',
        statement['var_type'] == 'HttpServletRequest',
    )):
        assertions['vars'][statement['var']] = {
            'untrusted': True,
        }


def get(statements: List[Statement]) -> None:
    assertions: Assertion = {
        'vars': {},
    }

    for statement in statements:
        statement_type = statement['type']

        if statement_type == 'BINDING':
            _binding_java_servlet_request(assertions, statement)
        elif statement_type == 'CALL':
            pass
        elif statement_type == 'CLASS_INSTANTIATION':
            pass
        elif statement_type == 'LITERAL':
            pass
        elif statement_type == 'LOOKUP':
            pass
        else:
            raise NotImplementedError(statement_type)
