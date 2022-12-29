from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.declaration_block import (
    build_declaration_block_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Iterator,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "declare")
    decl_id = match.get("__0__")
    if not decl_id:
        raise MissingCaseHandling(f"Bad ambient declaration in {args.n_id}")

    return build_declaration_block_node(args, cast(Iterator[NId], [decl_id]))
