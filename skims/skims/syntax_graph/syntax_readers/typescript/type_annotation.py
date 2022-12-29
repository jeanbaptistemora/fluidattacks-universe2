from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.typeof import (
    build_typeof_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, ":")
    type_id = match.get("__0__")
    if not type_id:
        raise MissingCaseHandling(f"Bad rest pattern in {args.n_id}")

    return build_typeof_node(args, type_id)
