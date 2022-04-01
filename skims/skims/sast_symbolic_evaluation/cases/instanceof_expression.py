from model import (
    graph_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
)


def evaluate(args: EvaluatorArgs) -> None:
    if (
        isinstance(args.dependencies[0], graph_model.SyntaxStepSymbolLookup)
        and (
            var_declaration := lookup_var_dcl_by_name(
                args,
                args.dependencies[0].symbol,
            )
        )
        and isinstance(var_declaration, graph_model.SyntaxStepDeclaration)
    ):
        args.syntax_step.meta.value = (
            var_declaration.var_type == args.syntax_step.instanceof_type
        )
