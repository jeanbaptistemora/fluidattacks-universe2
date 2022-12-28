from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter_list import (
    build_parameter_list_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)

    return build_parameter_list_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] not in {",", ":"}
        ),
    )
