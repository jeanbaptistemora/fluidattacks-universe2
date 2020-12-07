# Local libraries
from eval_java.model import (
    Statements,
)


def _is_linear_or_flatten_one_level(statements: Statements) -> bool:
    finished: bool = True
    statement_index = -1

    # pylint: disable=too-many-nested-blocks
    for statement in statements.copy():
        statement_index += 1

        # Already linearized this statement
        if statement.meta.linear:
            continue

        if statement.recursive:
            stack = 0

            if elem := getattr(statement, 'stack', None):
                stack_lists = [elem]
            elif elem := getattr(statement, 'stacks', None):
                stack_lists = elem
            else:
                stack_lists = []

            if stack_lists:
                for stack_list in stack_lists:
                    for arg in stack_list:
                        statements.insert(statement_index, arg)
                        statement_index += 1
                        stack += 1

                        if statement.recursive:
                            finished = False

                statement.meta.stack = -1 * stack
                statement.meta.linear = True
        else:
            statement.meta.linear = True
            statement.meta.stack = 0

    return finished


def linearize(statements: Statements) -> Statements:
    # Linearize one level until it's absolutely flattened
    while not _is_linear_or_flatten_one_level(statements):
        pass

    for statement in statements:
        for stack_name in ('stack', 'stacks'):
            if stack_list := getattr(statement, stack_name, []):
                stack_list.clear()

    return statements
