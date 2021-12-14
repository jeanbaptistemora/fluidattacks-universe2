from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_symbol_lookup_node(args: SyntaxGraphArgs, symbol: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        symbol=symbol,
        label_type="SymbolLookup",
    )

    return args.n_id
