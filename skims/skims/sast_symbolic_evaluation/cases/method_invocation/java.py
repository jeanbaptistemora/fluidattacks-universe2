from model.graph_model import (
    SyntaxStep,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def list_add(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    dcl.meta.value.append(args.dependencies[0])
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_remove(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    index = int(args.dependencies[0].meta.value)
    dcl.meta.value.pop(index)
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)
