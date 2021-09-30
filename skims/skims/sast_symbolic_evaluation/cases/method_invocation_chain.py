from model import (
    graph_model,
)
from sast_symbolic_evaluation.cases.method_invocation import (
    analyze_method_invocation,
    analyze_method_invocation_values,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    LookedUpClass,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def evaluate(args: EvaluatorArgs) -> None:
    # pylint: disable=expression-not-assigned
    (
        attempt_java_this_get_class(args)
        or attempt_java_this_get_class_get_class_loader(args)
        or attempt_java_class_loader_get_resource_as_stream(args)
        or attempt_metadata_java_class(args)
        or attempt_as_method_invocation(args)
        or attempt_as_object_instantiation(args)
    )


JAVA_THIS_GET_CLASS: str = "java.this.getClass()"


def attempt_java_this_get_class(args: EvaluatorArgs) -> bool:
    *_, base_var = args.dependencies

    if (
        isinstance(base_var, graph_model.SyntaxStepThis)
        and args.syntax_step.method == ".getClass"
    ):
        args.syntax_step.meta.value = JAVA_THIS_GET_CLASS
        return True

    return False


JAVA_CLASS_LOADER: str = "java.ClassLoader()"


def attempt_java_this_get_class_get_class_loader(
    args: EvaluatorArgs,
) -> bool:
    *_, base_var = args.dependencies

    if (
        base_var.meta.value == JAVA_THIS_GET_CLASS
        and args.syntax_step.method == ".getClassLoader"
    ):
        args.syntax_step.meta.value = JAVA_CLASS_LOADER
        return True

    return False


def attempt_java_class_loader_get_resource_as_stream(
    args: EvaluatorArgs,
) -> bool:
    *arguments, base_var = args.dependencies

    if (
        base_var.meta.value == JAVA_CLASS_LOADER
        and args.syntax_step.method == ".getResourceAsStream"
        and len(arguments) == 1
        and isinstance(arguments[0], graph_model.SyntaxStepLiteral)
    ):
        arg1 = arguments[0]
        if rsrc := args.graph_db.context.java_resources.get(arg1.meta.value):
            args.syntax_step.meta.value = rsrc
            return True

    return False


def attempt_metadata_java_class(args: EvaluatorArgs) -> bool:
    *arguments, var = args.dependencies

    if (
        isinstance(var.meta.value, LookedUpClass)
        and args.syntax_step.method in var.meta.value.metadata.methods
        and (
            return_step := args.eval_method(
                args,
                var.meta.value.metadata.methods[args.syntax_step.method].n_id,
                arguments,
                args.graph_db.shards_by_path_f(var.meta.value.shard_path),
            )
        )
    ):
        args.syntax_step.meta.danger = return_step.meta.danger
        args.syntax_step.meta.value = return_step.meta.value
        return True

    return False


def attempt_as_method_invocation(args: EvaluatorArgs) -> bool:
    *_, base_var = args.dependencies

    if isinstance(base_var, graph_model.SyntaxStepMethodInvocation):
        method = base_var.method + args.syntax_step.method
        analyze_method_invocation_values(args, method)

        if base_var.meta.danger:
            args.syntax_step.meta.danger = True
        else:
            analyze_method_invocation(args, method)

        return True

    if isinstance(base_var, graph_model.SyntaxStepThis):
        method = "this" + args.syntax_step.method
        analyze_method_invocation_values(args, method)
        analyze_method_invocation(args, method)

        return True

    if isinstance(base_var, graph_model.SyntaxStepMemberAccessExpression):
        base_var_str = node_to_str(args.shard.graph, base_var.meta.n_id)
        method = f"{base_var_str}.{args.syntax_step.method}"
        analyze_method_invocation(args, method)
        analyze_method_invocation_values(args, method)
        return True

    if isinstance(base_var, graph_model.SyntaxStepSymbolLookup):
        if var := lookup_var_dcl_by_name(args, base_var.symbol):
            method = var.var + "." + args.syntax_step.method
        else:
            method = base_var.symbol + "." + args.syntax_step.method
        analyze_method_invocation(args, method)
        analyze_method_invocation_values(args, method)
        return True

    if isinstance(base_var, graph_model.SyntaxStepParenthesizedExpression):
        args.syntax_step.meta.danger = base_var.meta.danger
        args.syntax_step.meta.value = base_var.meta.value
        return True

    return False


def attempt_as_object_instantiation(args: EvaluatorArgs) -> bool:
    *_, parent = args.dependencies

    if isinstance(parent, graph_model.SyntaxStepObjectInstantiation):
        method = parent.object_type + args.syntax_step.method
        analyze_method_invocation(args, method)
        analyze_method_invocation_values(args, method)
        return True

    return False
