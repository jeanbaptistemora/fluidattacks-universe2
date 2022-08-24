from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Dict,
    Optional,
)


def build_method_declaration_node(
    args: SyntaxGraphArgs,
    name: Optional[NId],
    block_id: NId,
    children: Dict[str, Optional[NId]],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        block_id=block_id,
        label_type="MethodDeclaration",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["name"] = name

    for name_node, node_id in children.items():
        if node_id:
            args.syntax_graph.nodes[args.n_id][name_node] = node_id
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(node_id)),
                label_ast="AST",
            )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    return args.n_id
