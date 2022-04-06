from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.interpolation import (
    build_interpolation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, *c_ids, _ = adj_ast(args.ast_graph, args.n_id)
    c_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"]
        in {"identifier", "member_access_expression"}
    ]
    return build_interpolation_node(args, c_ids)
