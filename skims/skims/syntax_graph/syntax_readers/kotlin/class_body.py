from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_body import (
    build_class_body_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    _, *c_ids, _ = adj_ast(graph, args.n_id)  # do not consider { }
    return build_class_body_node(args, c_ids)
