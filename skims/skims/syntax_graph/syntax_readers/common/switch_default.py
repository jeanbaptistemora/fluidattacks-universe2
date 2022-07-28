from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_default import (
    build_switch_default_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:

    if (
        expression := match_ast_d(
            args.ast_graph, args.n_id, "expression_statement"
        )
    ) or match_ast_d(args.ast_graph, args.n_id, "break_statement"):
        return build_switch_default_node(args, expression)

    raise MissingCaseHandling(f"Bad switch default handling in {args.n_id}")
