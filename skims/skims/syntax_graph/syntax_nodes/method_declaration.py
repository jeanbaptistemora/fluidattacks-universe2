from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Any,
    Optional,
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


def add_parameters(
    args: SyntaxGraphArgs,
    name_node: str,
    n_id: Any,
) -> SyntaxGraphArgs:
    args = add_main_node(args, name_node, n_id)

    return args


def build_method_declaration_node(
    args: SyntaxGraphArgs,
    name: Optional[str],
    block_id: Optional[NId],
    children: Any,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        label_type="MethodDeclaration",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["name"] = name

    for name_node, n_ids in children.items():
        if n_ids:
            if name_node == "attributes_id":
                args = add_attributes(args, name_node, n_ids)
            elif name_node == "parameters_id":
                args = add_parameters(args, name_node, n_ids)

    if block_id:
        args.syntax_graph.nodes[args.n_id]["block_id"] = block_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_id)),
            label_ast="AST",
        )

    return args.n_id
