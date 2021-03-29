# Local libraries
from model import (
    graph_model,
)
from sast.symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast.symbolic_evaluation.utils.generic import (
    lookup_var_dcl_by_name,
)


def evaluate(args: EvaluatorArgs) -> None:
    if isinstance(args.dependencies[0], graph_model.SyntaxStepSymbolLookup):
        if var_declaration := lookup_var_dcl_by_name(
            args,
            args.dependencies[0].symbol,
        ):
            args.syntax_step.meta.value = (
                var_declaration.var_type == args.syntax_step.instanceof_type
            )
