from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    List,
)


def build_element_binding_expression_node(
    args: SyntaxGraphArgs,
    childs: List[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="ElementBindingExpression",
    )
    for nid in childs:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(nid)),
            label_ast="AST",
        )

    return args.n_id
