from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.selector import (
    build_selector_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)
    return build_selector_node(args, iter(c_ids))
