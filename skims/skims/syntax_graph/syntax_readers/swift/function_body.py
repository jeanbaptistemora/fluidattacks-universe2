from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.function_body import (
    build_function_body_node,
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
    return build_function_body_node(args, iter(c_ids))
