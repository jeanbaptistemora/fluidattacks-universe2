from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_export_statement_node(
    args: SyntaxGraphArgs,
    expression: Optional[str],
    exported_block: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Export",
    )

    if expression:
        args.syntax_graph.nodes[args.n_id]["expression"] = expression

    if exported_block:
        args.syntax_graph.nodes[args.n_id]["declaration_id"] = exported_block
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(exported_block)),
            label_ast="AST",
        )

    return args.n_id
