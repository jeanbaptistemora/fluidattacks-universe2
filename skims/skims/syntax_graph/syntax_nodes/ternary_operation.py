from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_ternary_operation_node(
    args: SyntaxGraphArgs,
    condition_id: NId,
    alternative_id: NId,
    consequence_id: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        condition_id=condition_id,
        alternative_id=alternative_id,
        consequence_id=consequence_id,
        label_type="TernaryOperation",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(condition_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(alternative_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(consequence_id)),
        label_ast="AST",
    )

    return args.n_id
