from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.accessor_declaration import (
    build_accessor_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs = g.adj(args.ast_graph, args.n_id)
    var_type = args.ast_graph.nodes[childs[0]]["label_type"]
    block = (
        childs[1]
        if args.ast_graph.nodes[childs[1]]["label_type"] == "block"
        else None
    )
    return build_accessor_declaration_node(args, var_type, block)
