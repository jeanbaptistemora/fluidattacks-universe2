from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:

    m_childs = match_ast(
        args.ast_graph,
        args.n_id,
    )

    node_types = {"decimal_integer_literal", "string", "identifier", "object"}

    childs = [
        child
        for child in m_childs.values()
        if args.ast_graph.nodes[child]["label_type"] in node_types
    ]

    c_ids = list(filter(None, childs))

    if len(m_childs) > 2 and not childs:
        raise MissingCaseHandling(f"Bad array handling in {args.n_id}")

    return build_array_node(args, c_ids)
