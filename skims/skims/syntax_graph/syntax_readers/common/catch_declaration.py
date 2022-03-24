from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.catch_declaration import (
    build_catch_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, *c_ids, _ = adj_ast(args.ast_graph, args.n_id)  # do not consider ( )
    return build_catch_declaration_node(args, c_ids)
