# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Lookup the symbol in the stack
    for symbol in common.read_stack_symbols(statements, index):
        symbol_var_no_index = symbol.var.split('[', maxsplit=1)[0]
        statement_var_no_index = statement.symbol.split('[', maxsplit=1)[0]

        if symbol_var_no_index == statement_var_no_index:
            statement.meta.danger = symbol.meta.danger
            statement.meta.value = symbol.meta.value
            return

    # Not found
    statement.meta.danger = False
