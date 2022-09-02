from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    get_brother_node,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    if (
        body_id := get_brother_node(args.ast_graph, args.n_id, "function_body")
    ) and (
        parameters_id := match_ast_d(
            args.ast_graph, args.n_id, "formal_parameter_list"
        )
    ):
        function_name = node_to_str(args.ast_graph, name_id)
        return build_method_declaration_node(
            args, function_name, body_id, {"parameters_id": parameters_id}
        )

    raise MissingCaseHandling(
        f"Bad function signature handling in {args.n_id}"
    )
