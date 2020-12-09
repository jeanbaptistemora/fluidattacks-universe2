# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]

    chain, *args = common.read_stack(statements, index)

    # Analyze if the arguments involved in the chain are dangerous
    chain_danger = chain.meta.danger

    # Analyze if the arguments involved in the function are dangerous
    args_danger = any(arg.meta.danger for arg in args)

    # Analyze if the call itself is sensitive
    method = statement.method
    call_danger = any((
        # Known function to return user controlled data
        method.endswith('.setAttribute'),
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
    statement.meta.danger = chain_danger or args_danger or call_danger
