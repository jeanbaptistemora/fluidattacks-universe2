from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declarator import (
    build_variable_declarator_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    variable_name = node_to_str(
        args.ast_graph, args.ast_graph.nodes[args.n_id]["label_field_name"]
    )
    value_id = args.ast_graph.nodes[args.n_id].get("label_field_value")
    if not value_id:
        raise MissingCaseHandling(
            f"Bad variable declarator handling in {args.n_id}"
        )

    return build_variable_declarator_node(args, variable_name, value_id)
