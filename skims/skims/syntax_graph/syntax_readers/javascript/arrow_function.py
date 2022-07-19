from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.arrow_function import (
    build_arrow_function_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    arrow_id = args.ast_graph.nodes[args.n_id]
    block_id = arrow_id["label_field_body"]
    if (params := arrow_id.get("label_field_parameter")) or (
        params := arrow_id.get("label_field_parameters")
    ):
        return build_arrow_function_node(args, block_id, params)

    return build_arrow_function_node(args, block_id, None)
