from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.identifier_list import (
    build_identifier_list_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)
    var_types = {"initialized_identifier", "static_final_declaration"}
    filtered_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] in var_types
    ]
    if len(filtered_ids) == 1:
        return args.generic(args.fork_n_id(filtered_ids[0]))

    return build_identifier_list_node(args, iter(filtered_ids))
