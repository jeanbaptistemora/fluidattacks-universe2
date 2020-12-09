# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze if the arguments involved in the function are dangerous
    args = common.read_stack(statements, index)
    args_danger = any(arg.meta.danger for arg in args)

    # Analyze if the call itself is sensitive
    method = statement.method
    call_danger = any((
        # Known function to return user controlled data
        method.endswith('.getCookies'),
        method.endswith('.getSession'),
        # Use of a method from a dangerous symbol
        any(
            method_start.startswith(symbol.var)
            for method_start in [method.split('.')[0]]
            for symbol in common.read_stack_symbols(statements, index)
            if symbol.meta.danger
        ),
        method in {
            'java.lang.Math.random',
            'lang.Math.random',
            'Math.random',
            'random',
        }
    ))

    # Local context
    statement.meta.danger = args_danger or call_danger
