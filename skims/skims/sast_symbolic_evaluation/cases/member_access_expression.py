from model.graph_model import (
    SyntaxStepMemberAccessExpression,
    SyntaxStepSymbolLookup,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    dependency = args.dependencies[0]
    step: SyntaxStepMemberAccessExpression = args.syntax_step
    if (
        isinstance(dependency, SyntaxStepSymbolLookup)
        and (value := dependency.meta.value)
        and isinstance(dependency.meta.value, dict)
    ):
        if member_value := value.get(step.member):
            step.meta.danger = member_value.meta.danger
            step.meta.value = member_value.meta.value

    else:
        step.meta.danger = dependency.meta.danger
