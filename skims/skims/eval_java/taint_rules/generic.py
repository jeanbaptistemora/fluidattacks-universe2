# Standard library
import json

# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    add,
    binding,
    call,
    class_instantiation,
    literal,
    lookup,
)
from utils.logs import (
    blocking_log,
)


def taint(statements: Statements) -> None:
    for index, statement in enumerate(statements):
        statement['__danger__'] = None
        statement_type = statement['type']

        if statement_type == 'ADD':
            add.taint(statements, index)
        elif statement_type == 'BINDING':
            binding.taint(statements, index)
        elif statement_type == 'CALL':
            call.taint(statements, index)
        elif statement_type == 'CLASS_INSTANTIATION':
            class_instantiation.taint(statements, index)
        elif statement_type == 'LITERAL':
            literal.taint(statement)
        elif statement_type == 'LOOKUP':
            lookup.taint(statements, index)
        else:
            raise NotImplementedError(statement_type)

    # Debugging information, only visible with skims --debug
    blocking_log('debug', '%s', json.dumps(statements, indent=2))
