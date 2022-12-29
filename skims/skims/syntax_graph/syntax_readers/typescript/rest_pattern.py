from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.rest_pattern import (
    build_rest_pattern_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "...")
    identifier_id = match.get("__0__")
    if not identifier_id:
        raise MissingCaseHandling(f"Bad rest pattern in {args.n_id}")

    return build_rest_pattern_node(args, identifier_id)
