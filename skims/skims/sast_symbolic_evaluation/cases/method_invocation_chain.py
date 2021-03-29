# Local libraries
from model import graph_model
from sast_symbolic_evaluation.cases.method_invocation import (
    analyze_method_invocation,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    *method_arguments, parent = args.dependencies

    if isinstance(parent.meta.value, graph_model.GraphShardMetadataJavaClass):
        if args.syntax_step.method in parent.meta.value.methods:
            method = parent.meta.value.methods[args.syntax_step.method]
            if return_step := args.eval_method(
                args, method.n_id, method_arguments,
            ):
                args.syntax_step.meta.danger = return_step.meta.danger
                args.syntax_step.meta.value = return_step.meta.value
    elif isinstance(parent, graph_model.SyntaxStepMethodInvocation):
        method = parent.method + args.syntax_step.method
        analyze_method_invocation(args, method)
    elif isinstance(parent, graph_model.SyntaxStepObjectInstantiation):
        method = parent.object_type + args.syntax_step.method
        analyze_method_invocation(args, method)
