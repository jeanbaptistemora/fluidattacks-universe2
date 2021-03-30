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
    # pylint: disable=expression-not-assigned
    (
        attempt_java_this_get_class(args) or
        attempt_java_this_get_class_get_class_loader(args) or
        attempt_java_class_loader_get_resource_as_stream(args) or
        attempt_the_old_way(args)
    )


JAVA_THIS_GET_CLASS: str = 'java.this.getClass()'


def attempt_java_this_get_class(args: EvaluatorArgs) -> bool:
    *_, parent = args.dependencies

    if isinstance(parent, graph_model.SyntaxStepThis):
        if args.syntax_step.method == '.getClass':
            args.syntax_step.meta.value = JAVA_THIS_GET_CLASS
            return True

    return False


JAVA_CLASS_LOADER: str = 'java.ClassLoader()'


def attempt_java_this_get_class_get_class_loader(
    args: EvaluatorArgs,
) -> bool:
    *_, parent = args.dependencies

    if parent.meta.value == JAVA_THIS_GET_CLASS:
        if args.syntax_step.method == '.getClassLoader':
            args.syntax_step.meta.value = JAVA_CLASS_LOADER
            return True

    return False


def attempt_java_class_loader_get_resource_as_stream(
    args: EvaluatorArgs,
) -> bool:
    *parent_arguments, parent = args.dependencies

    if (
        parent.meta.value == JAVA_CLASS_LOADER
        and args.syntax_step.method == '.getResourceAsStream'
        and len(parent_arguments) == 1
        and isinstance(parent_arguments[0], graph_model.SyntaxStepLiteral)
    ):
        arg1 = parent_arguments[0]
        if rsrc := args.graph_db.context.java_resources.get(arg1.meta.value):
            args.syntax_step.meta.value = rsrc
            return True

    return False


def attempt_the_old_way(args: EvaluatorArgs) -> bool:
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

    return False
