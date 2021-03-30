# Standard library
from typing import (
    Optional,
)

# Local libraries
from model import (
    graph_model,
)
from sast_symbolic_evaluation.cases.method_invocation import (
    analyze_method_invocation,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    (
        attempt_java_this_get_class(args) or
        attempt_the_old_way(args)
    )


JAVA_THIS_GET_CLASS: str = 'java.this.getClass()'


def attempt_java_this_get_class(args: EvaluatorArgs) -> Optional[bool]:
    *_, parent = args.dependencies

    if isinstance(parent, graph_model.SyntaxStepThis):
        if args.syntax_step.method == '.getClass':
            args.syntax_step.meta.value = JAVA_THIS_GET_CLASS
            return True


def attempt_the_old_way(args: EvaluatorArgs) -> Optional[bool]:
    *method_arguments, parent = args.dependencies

    if isinstance(parent.meta.value, graph_model.GraphShardMetadataJavaClass):
        if args.syntax_step.method in parent.meta.value.methods:
            method = parent.meta.value.methods[args.syntax_step.method]
            if return_step := args.eval_method(
                args, method.n_id, method_arguments,
            ):
                args.syntax_step.meta.danger = return_step.meta.danger
                args.syntax_step.meta.value = return_step.meta.value
                return True

    if isinstance(parent, graph_model.SyntaxStepMethodInvocation):
        method = parent.method + args.syntax_step.method
        analyze_method_invocation(args, method)
        return True

    if isinstance(parent, graph_model.SyntaxStepObjectInstantiation):
        method = parent.object_type + args.syntax_step.method
        analyze_method_invocation(args, method)
        return True
