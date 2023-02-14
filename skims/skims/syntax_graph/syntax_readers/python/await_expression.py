from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.await_expression import (
    build_await_expression_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "await")

    if len(match) == 2:
        expression = str(match["__0__"])
        return build_await_expression_node(args, expression)

    raise MissingCaseHandling(f"Bad else handling in {args.n_id}")
