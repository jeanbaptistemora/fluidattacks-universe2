from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.modifiers import (
    build_modifiers_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs = adj_ast(graph, args.n_id)
    dec_ids = [childs[-1]]

    return build_modifiers_node(args, dec_ids)
