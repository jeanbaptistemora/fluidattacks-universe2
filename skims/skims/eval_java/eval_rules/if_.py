# Local libraries
from eval_java.model import (
    Statements,
    StopEvaluation,
)
from eval_java.eval_rules import (
    common,
)


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze the arguments involved in the expression
    if stack := common.read_stack(statements, index):
        predicate, = stack

        if ((
            # Truthy path
            statement.cfg_condition == {'cfg_always', 'cfg_true'}
            and predicate.meta.value is True
        ) or (
            # Falsy path
            statement.cfg_condition in {'cfg_false', 'cfg_never'}
            and predicate.meta.value is False
        ) or (
            # We can't know at compile time, so let's check it for completeness
            predicate.meta.value is None
        )):
            # Integrity check passed
            pass
        else:
            # We are following a path that won't happen
            raise StopEvaluation()
