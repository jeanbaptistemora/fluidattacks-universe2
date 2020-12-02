# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Lookup the symbol in the stack
    for symbol in common.read_stack_symbols(statements, index):
        if symbol.var == statement.symbol:
            statement.meta.danger = symbol.meta.danger
            return

    # Not found
    statement.meta.danger = False
