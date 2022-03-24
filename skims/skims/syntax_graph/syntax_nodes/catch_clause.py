from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_catch_clause_node(
    args: SyntaxGraphArgs,
    block_node: NId,
    catch_declaration_block: Optional[NId],
    catch_filter_clause_block: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block_node,
        label_type="CatchClause",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_node)),
        label_ast="AST",
    )

    if catch_declaration_block:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(catch_declaration_block)),
            label_ast="AST",
        )

    if catch_filter_clause_block:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(catch_filter_clause_block)),
            label_ast="AST",
        )

    return args.n_id
