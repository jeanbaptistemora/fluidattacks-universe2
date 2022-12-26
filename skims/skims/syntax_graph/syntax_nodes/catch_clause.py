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
    block_node: Optional[NId],
    catch_declaration_block: Optional[NId],
    catch_filter_clause_block: Optional[NId],
    parameters_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="CatchClause",
    )

    if block_node:
        args.syntax_graph.nodes[args.n_id]["block_id"] = block_node
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

    if parameters_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(parameters_id)),
            label_ast="AST",
        )

    return args.n_id
