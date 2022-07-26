from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_else_clause_node(
    args: SyntaxGraphArgs,
    child: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="ElseClause",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(child)),
        label_ast="AST",
    )

    return args.n_id
