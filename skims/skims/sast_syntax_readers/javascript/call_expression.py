from model import (
    graph_model,
)
from model.graph_model import (
    CurrentInstance,
    SyntaxStepMeta,
    SyntaxStepMethodInvocation,
    SyntaxStepMethodInvocationChain,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from typing import (
    List,
    Optional,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    get_identifiers_ids_js,
    node_to_str,
)


def _pred_calls(args: SyntaxReaderArgs, function_id: str) -> List[str]:
    nested_calls: List[str] = []
    member_exp = "member_expression"
    for n_id in get_identifiers_ids_js(args.graph, function_id, member_exp):
        for pred_id in g.pred_ast_lazy(args.graph, n_id, depth=2):
            if args.graph.nodes[pred_id]["label_type"] == "call_expression":
                if pred_id not in nested_calls:
                    nested_calls.append(pred_id)
                break
    return list(reversed(nested_calls))


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    arguments_id = node_attrs["label_field_arguments"]
    function_id = node_attrs["label_field_function"]
    function_attrs = args.graph.nodes[function_id]
    method_name: Optional[str] = None

    if function_attrs["label_type"] == "member_expression":
        nested_methods_keys = node_to_str(args.graph, function_id).split(".")

        nested_calls = _pred_calls(args, function_id)
        if len(nested_calls) > 1:
            yield SyntaxStepMethodInvocationChain(
                meta=graph_model.SyntaxStepMeta.default(
                    args.n_id,
                    [
                        args.generic(args.fork_n_id(nested_calls[1])),
                        *dependencies_from_arguments(
                            args.fork_n_id(
                                args.graph.nodes[args.n_id][
                                    "label_field_arguments"
                                ]
                            ),
                        ),
                    ],
                ),
                method=nested_methods_keys[-1],
            )
        else:
            method_name = node_to_str(args.graph, function_id)

    if not method_name and function_attrs["label_type"] == "identifier":
        method_name = args.graph.nodes[function_id]["label_text"]

    if method_name:
        yield SyntaxStepMethodInvocation(
            meta=SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(
                    args.fork_n_id(arguments_id),
                ),
            ),
            method=method_name,
            current_instance=CurrentInstance(fields={}),
        )
