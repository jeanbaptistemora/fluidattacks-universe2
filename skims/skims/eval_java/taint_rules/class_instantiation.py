
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
    args_danger = any(arg['__danger__'] for arg in args)

    # Analyze if the instantiation itself is sensitive
    call_danger = any((
        all((
            statement['class_type'] in {'java.io.File'},
            statement.get('sink') == 'F063_PATH_TRAVERSAL',
        )),
    ))

    # Local context
    statement['__danger__'] = call_danger and args_danger
