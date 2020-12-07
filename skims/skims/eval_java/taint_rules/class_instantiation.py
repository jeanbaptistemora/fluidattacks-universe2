
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

    # Analyze if the instantiation itself is sensitive
    call_danger = any((
        all((
            statement.class_type in {
                'java.io.File',
                'io.File',
                'File',

                'java.io.FileOutputStream',
                'io.FileOutputStream',
                'FileOutputStream',
            },
            statement.meta.sink == 'F063_PATH_TRAVERSAL',
        )),
    ))

    # Local context
    statement.meta.danger = call_danger and args_danger
