from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.using_statement import (
    build_using_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    if match := match_ast_d(args.ast_graph, args.n_id, "variable_declaration"):
        return build_using_statement_node(args, match)

    raise MissingCaseHandling(f"Bad using statement handling in {args.n_id}")
