
# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
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

                'java.io.FileInputStream',
                'io.FileInputStream',
                'FileInputStream',
            },
            statement.meta.sink == 'F063_PATH_TRAVERSAL',
        )),
        all((
            statement.class_type in {
                'java.util.Random',
                'util.Random',
                'Random',
            },
            statement.meta.sink == 'F034_INSECURE_RANDOMS',
        )),
    ))

    # Local context
    if call_danger:
        statement.meta.danger = args_danger if args else True
    else:
        statement.meta.danger = args_danger
