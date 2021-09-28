from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils.graph.text_nodes import (
    get_text_childs,
    n_ids_to_str,
)
from utils.string import (
    split_on_first_dot,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    args_id = args.graph.nodes[args.n_id]["label_field_arguments"]
    expression_id = args.graph.nodes[args.n_id]["label_field_function"]
    expression_type = args.graph.nodes[expression_id]["label_type"]

    if not args_id:
        raise MissingCaseHandling(args)

    if expression_type == "identifier":
        yield graph_model.SyntaxStepMethodInvocation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(
                    args.fork_n_id(args_id),
                ),
            ),
            method=args.graph.nodes[expression_id]["label_text"],
            current_instance=graph_model.CurrentInstance(fields={}),
        )
    elif expression_type == "member_access_expression":
        n_ids = get_text_childs(args.graph, expression_id)
        access_expression = n_ids_to_str(args.graph, n_ids)
        _, method_name = split_on_first_dot(access_expression)

        base_ident, *_ = n_ids

        yield graph_model.SyntaxStepMethodInvocationChain(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(base_ident)),
                    *dependencies_from_arguments(
                        args.fork_n_id(args_id),
                    ),
                ],
            ),
            method=method_name,
        )
    else:
        raise MissingCaseHandling(args)
