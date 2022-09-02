from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.type_identifier import (
    build_symbol_type_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    symbol_type = args.ast_graph.nodes[args.n_id]["label_text"]
    return build_symbol_type_node(args, symbol_type)
