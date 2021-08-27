from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    SyntaxStepArrayInstantiation,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    step: SyntaxStepArrayInstantiation = args.syntax_step
    dangert_types = {
        FindingEnum.F052: {
            "byte",
        }
    }
    step.meta.danger = step.array_type in dangert_types.get(
        args.finding, set()
    )
    step.meta.danger = step.meta.danger or any(
        dep.meta.danger for dep in args.dependencies
    )
