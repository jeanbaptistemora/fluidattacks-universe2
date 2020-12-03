# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    common,
)


def taint(statements: Statements, index: int) -> None:
    statement = statements[index]
    var_type = statement.var_type

    # Analyze the arguments involved in the assignment
    args = common.read_stack(statements, index)
    args_danger = any(arg.meta.danger for arg in args)

    # Analyze if the binding itself is sensitive
    bind_danger = any((
        # This type is an HTTP request from JavaX framework
        var_type == 'HttpServletRequest',
    ))

    # Local context
    statement.meta.danger = bind_danger or args_danger
