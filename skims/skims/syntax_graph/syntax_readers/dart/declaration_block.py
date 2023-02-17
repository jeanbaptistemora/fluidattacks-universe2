from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.declaration_block import (
    build_declaration_block_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(args.ast_graph, args.n_id)
    if graph.nodes[c_ids[-1]]["label_type"] == "static_final_declaration_list":
        return args.generic(args.fork_n_id(c_ids[-1]))
    invalid_childs = {"?", ";"}
    return build_declaration_block_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] not in invalid_childs
        ),
    )
