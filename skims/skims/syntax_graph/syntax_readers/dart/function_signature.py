from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.function_signature import (
    build_function_signature_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    function_name = node_to_str(args.ast_graph, name_id)
    if parameters_id := match_ast_d(
        args.ast_graph, args.n_id, "formal_parameter_list"
    ):
        return build_function_signature_node(
            args, function_name, parameters_id
        )

    raise MissingCaseHandling(
        f"Bad function signature handling in {args.n_id}"
    )
