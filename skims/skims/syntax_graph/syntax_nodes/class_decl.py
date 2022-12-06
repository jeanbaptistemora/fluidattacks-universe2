from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Any,
)
from utils.graph import (
    match_ast_d,
)


def add_main_node(
    args: SyntaxGraphArgs, name_node: str, n_id: Any
) -> SyntaxGraphArgs:
    args.syntax_graph.nodes[args.n_id][name_node] = n_id
    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(n_id)),
        label_ast="AST",
    )
    return args


def add_attributes(
    args: SyntaxGraphArgs,
    name_node: str,
    childs: Any,
) -> SyntaxGraphArgs:
    args = add_main_node(args, name_node, childs[0])

    for attribute_branch in childs[1:]:
        attribute = match_ast_d(args.ast_graph, attribute_branch, "attribute")
        if attribute:
            args.syntax_graph.add_edge(
                childs[0],
                args.generic(args.fork_n_id(attribute)),
                label_ast="AST",
            )
    return args


def build_class_node(
    args: SyntaxGraphArgs,
    name: str,
    block_id: NId,
    attributes_id: Any,
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

    if attributes_id:
        args = add_attributes(args, name, attributes_id)

    return args.n_id
