from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.symbol_lookup import (
    build_symbol_lookup_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    symbol = node_to_str(args.ast_graph, args.n_id)
    return build_symbol_lookup_node(args, symbol)
