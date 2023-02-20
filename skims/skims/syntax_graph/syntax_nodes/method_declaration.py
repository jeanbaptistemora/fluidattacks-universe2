from collections.abc import (
    Iterable,
    Mapping,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_method_declaration_node(
    args: SyntaxGraphArgs,
    name: str | None,
    block_id: NId | None,
    children: Mapping[str, Iterable[NId]],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="MethodDeclaration",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["name"] = name

    if block_id:
        args.syntax_graph.nodes[args.n_id]["block_id"] = block_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_id)),
            label_ast="AST",
        )

    for name_node, n_ids in children.items():
        if n_ids:
            if len(list(n_ids)) == 1:
                args.syntax_graph.nodes[args.n_id][name_node] = list(n_ids)[0]
                args.syntax_graph.add_edge(
                    args.n_id,
                    args.generic(args.fork_n_id(list(n_ids)[0])),
                    label_ast="AST",
                )
            elif len(list(n_ids)) > 1:
                for attrlist_id in n_ids:
                    args.syntax_graph.add_edge(
                        args.n_id,
                        args.generic(args.fork_n_id(attrlist_id)),
                        label_ast="AST",
                    )

    return args.n_id
