# Local libraries
from eval_java.model import (
    Statements,
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


def _is_linear_or_flatten_one_level(statements: Statements) -> bool:
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
            for stack_name in ('stack', 'stack_0', 'stack_1'):
                if stack_name not in statement:
                    continue

                for arg in statement[stack_name]:
                    arg_type = arg['type']

                    if arg_type in RECURSIVE or arg_type in NON_RECURSIVE:
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


def linearize(statements: Statements) -> Statements:
    # Linearize one level until it's absolutely flattened
    while not _is_linear_or_flatten_one_level(statements):
        pass

    # Remove temporary meta data
    for statement in statements:
        statement.pop('__linear__', None)

    return statements
