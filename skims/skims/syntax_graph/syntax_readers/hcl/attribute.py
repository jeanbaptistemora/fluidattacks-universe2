from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.pair import (
    build_pair_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    key_id = args.ast_graph.nodes[args.n_id].get("label_field_key")
    if not key_id:
        key_id = str(match_ast_d(graph, args.n_id, "identifier"))
    value_id = args.ast_graph.nodes[args.n_id].get("label_field_val")
    if not value_id:
        value_id = str(match_ast_d(graph, args.n_id, "expression"))

    return build_pair_node(args, key_id, value_id)
