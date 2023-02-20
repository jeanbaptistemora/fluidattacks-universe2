from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_using_statement_node(
    args: SyntaxGraphArgs,
    block_id: NId,
    declaration_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block_id,
        label_type="UsingStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    if declaration_id:
        args.syntax_graph.nodes[args.n_id]["declaration_id"] = declaration_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(declaration_id)),
            label_ast="AST",
        )

    return args.n_id
