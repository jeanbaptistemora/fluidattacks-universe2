from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Dict,
    List,
)
from utils.graph import (
    match_ast_d,
)


def build_class_node(
    args: SyntaxGraphArgs,
    name: str,
    block_id: NId,
    children: Dict[str, List[NId]],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        block_id=block_id,
        label_type="Class",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    for name_node, n_ids in children.items():
        if n_ids:
            args.syntax_graph.nodes[args.n_id][name_node] = n_ids[0]
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(n_ids[0])),
                label_ast="AST",
            )

            for attribute_branch in n_ids[1:]:
                attribute = match_ast_d(
                    args.ast_graph, attribute_branch, "attribute"
                )
                if attribute:
                    args.syntax_graph.add_edge(
                        n_ids[0],
                        args.generic(args.fork_n_id(attribute)),
                        label_ast="AST",
                    )

    return args.n_id
