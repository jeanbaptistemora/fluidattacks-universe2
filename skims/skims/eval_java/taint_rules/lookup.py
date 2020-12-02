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
        if symbol['var'] == statement['symbol']:
            statement['__danger__'] = symbol['__danger__']
            return

    # Not found
    statement['__danger__'] = False
