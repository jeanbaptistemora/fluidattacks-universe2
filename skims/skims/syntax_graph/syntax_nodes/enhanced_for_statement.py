from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_enhanced_for_statement_node(
    args: SyntaxGraphArgs,
    type_str: str,
    name_str: str,
    value_node: str,
    body_node: str,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        identifier_type=type_str,
        identifier_name=name_str,
        value_id=value_node,
        body_id=body_node,
        label_type="EnhancedForStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(value_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(body_node)),
        label_ast="AST",
    )

    return args.n_id
